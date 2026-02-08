"""
API路由 - 批量处理
"""
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
import os
import uuid

from app.database import get_db
from app.services.batch_service import BatchService
from app.services.image_service import ImageService

router = APIRouter()
batch_service = BatchService()
image_service = ImageService()


@router.post("/batch/ocr")
async def batch_ocr(
    files: list[UploadFile] = File(...),
    lang: str = Form("ch"),
    current_user = Depends(lambda: None)  # TODO: 添加认证
):
    """
    批量OCR识别
    """
    try:
        # 保存所有文件
        image_paths = []
        for file in files:
            temp_path = await image_service.save_upload_file(file)
            image_paths.append(temp_path)

        # 批量OCR
        results = await batch_service.batch_ocr(image_paths, lang)

        # 删除临时文件
        for path in image_paths:
            os.unlink(path)

        return {
            "success": True,
            "data": {
                "total": len(files),
                "results": results
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量OCR失败: {str(e)}"
        )


@router.post("/batch/enhance")
async def batch_enhance(
    files: list[UploadFile] = File(...),
    current_user = Depends(lambda: None)
):
    """
    批量图像增强
    """
    try:
        # 保存所有文件
        image_paths = []
        for file in files:
            temp_path = await image_service.save_upload_file(file)
            image_paths.append(temp_path)

        # 批量增强
        enhanced_paths = await batch_service.batch_enhance(image_paths)

        # 返回增强后的图片URL
        enhanced_urls = [
            path.replace("static", "/static") for path in enhanced_paths
        ]

        # 删除原始文件
        for path in image_paths:
            os.unlink(path)

        return {
            "success": True,
            "data": {
                "total": len(files),
                "enhanced_urls": enhanced_urls
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量增强失败: {str(e)}"
        )


@router.post("/batch/export-pdf")
async def batch_export_pdf(
    files: list[UploadFile] = File(...),
    filename: str = Form(None),
    current_user = Depends(lambda: None)
):
    """
    批量导出为单个PDF
    """
    try:
        # 保存所有文件
        image_paths = []
        for file in files:
            temp_path = await image_service.save_upload_file(file)
            image_paths.append(temp_path)

        # 生成文件名
        if filename is None:
            filename = f"batch_{uuid.uuid4().hex[:8]}.pdf"

        # 批量导出PDF
        pdf_path = await batch_service.batch_pdf_export(image_paths, filename)

        # 删除临时图片
        for path in image_paths:
            os.unlink(path)

        return {
            "success": True,
            "data": {
                "pdf_url": pdf_path
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"批量导出PDF失败: {str(e)}"
        )
