"""
API路由 - 证件扫描
"""
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
import os
import uuid

from app.database import get_db
from app.models import Document, IDCard
from app.services.ocr_service import OCRService
from app.services.image_service import ImageService

router = APIRouter()
ocr_service = OCRService()
image_service = ImageService()


@router.post("/id-card/scan")
async def scan_id_card(
    file: UploadFile = File(...),
    card_type: str = Form("id_card"),  # id_card/passport/license/等
    enhance: bool = Form(True),
    auto_crop: bool = Form(True),
    user_id: str = Form("default"),
    db: Session = Depends(get_db)
):
    """
    证件扫描
    """
    try:
        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        # 处理图像
        processed_path = await image_service.process_document(
            temp_path,
            enhance=enhance,
            auto_crop=auto_crop
        )

        # OCR识别
        ocr_result = await ocr_service.ocr_image(processed_path, "ch")

        # 提取证件信息（简化版，实际需要根据不同证件类型解析）
        id_info = extract_id_info(card_type, ocr_result)

        # 保存到数据库
        document = Document(
            user_id=user_id,
            name=f"{card_type}_{uuid.uuid4().hex[:8]}",
            type=card_type,
            file_path=processed_path,
            ocr_result=ocr_result,
            metadata={"file_size": os.path.getsize(processed_path)},
            status="success"
        )
        db.add(document)
        db.commit()
        db.refresh(document)

        # 保存证件信息
        id_card = IDCard(
            user_id=user_id,
            document_id=document.id,
            card_type=card_type,
            raw_data=ocr_result,
            **id_info
        )
        db.add(id_card)
        db.commit()

        # 删除临时文件
        os.unlink(temp_path)

        return {
            "success": True,
            "data": {
                "document_id": document.id,
                "card_type": card_type,
                "image_url": processed_path.replace("static", "/static"),
                "ocr_result": ocr_result,
                "id_info": id_info
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"证件扫描失败: {str(e)}"
        )


def extract_id_info(card_type: str, ocr_result: dict) -> dict:
    """
    提取证件信息
    """
    text = ocr_result.get("text", "")
    texts = ocr_result.get("texts", [])

    info = {}

    # 根据证件类型提取信息（简化版，实际需要更复杂的解析）
    if card_type == "id_card":
        # 身份证信息提取（简化）
        info = {
            "name": extract_from_text(text, ["姓名", "Name"]),
            "id_number": extract_from_text(text, ["身份证", "ID"]),
            "address": extract_from_text(text, ["地址", "Address"])
        }
    elif card_type == "passport":
        # 护照信息提取（简化）
        info = {
            "name": extract_from_text(text, ["姓名", "Name"]),
            "id_number": extract_from_text(text, ["护照", "Passport"])
        }
    elif card_type == "license":
        # 驾驶证信息提取（简化）
        info = {
            "name": extract_from_text(text, ["姓名", "Name"]),
            "id_number": extract_from_text(text, ["驾驶证", "License"])
        }
    elif card_type == "graduation":
        # 毕业证信息提取（简化）
        info = {
            "name": extract_from_text(text, ["姓名", "Name"]),
            "id_number": extract_from_text(text, ["学号", "ID"])
        }
    elif card_type == "student_card":
        # 学生证信息提取（简化）
        info = {
            "name": extract_from_text(text, ["姓名", "Name"]),
            "id_number": extract_from_text(text, ["学号", "ID"])
        }

    return info


def extract_from_text(text: str, keywords: list) -> str:
    """从文本中提取关键词后的内容"""
    for keyword in keywords:
        if keyword in text:
            idx = text.find(keyword)
            if idx != -1:
                # 提取关键词后的内容
                remaining = text[idx + len(keyword):].strip()
                # 简单提取第一行
                lines = remaining.split("\n")
                if lines:
                    return lines[0].strip()
    return ""
