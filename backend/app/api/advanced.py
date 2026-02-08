"""
API路由 - 高级功能
"""
from fastapi import APIRouter, Depends, File, UploadFile, Form, HTTPException, status
from sqlalchemy.orm import Session
import os

from app.database import get_db
from app.services.image_service import ImageService
from app.services.watermark_service import WatermarkService
from app.services.translation_service import TranslationService
from app.services.office_service import OfficeService
from app.services.long_image_service import LongImageService

router = APIRouter()
image_service = ImageService()
watermark_service = WatermarkService()
translation_service = TranslationService()
office_service = OfficeService()
long_image_service = LongImageService()


@router.post("/advanced/remove-watermark")
async def remove_watermark(
    file: UploadFile = File(...),
    watermark_type: str = Form("text"),  # text/logo
    watermark_text: str = Form(None),
    current_user = Depends(lambda: None)
):
    """
    去水印
    """
    try:
        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        # 去水印
        if watermark_type == "text":
            result_path = watermark_service.remove_text_watermark(
                temp_path,
                watermark_text
            )
        else:  # logo
            result_path = watermark_service.remove_logo_watermark(temp_path)

        # 删除临时文件
        if temp_path != result_path:
            os.unlink(temp_path)

        return {
            "success": True,
            "data": {
                "image_url": result_path.replace("static", "/static")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"去水印失败: {str(e)}"
        )


@router.post("/advanced/add-watermark")
async def add_watermark(
    file: UploadFile = File(...),
    watermark_text: str = Form("智扫通"),
    position: str = Form("bottom_right"),
    opacity: float = Form(0.3),
    current_user = Depends(lambda: None)
):
    """
    添加水印
    """
    try:
        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        # 添加水印
        result_path = watermark_service.add_watermark(
            temp_path,
            watermark_text,
            position,
            opacity
        )

        # 删除临时文件
        if temp_path != result_path:
            os.unlink(temp_path)

        return {
            "success": True,
            "data": {
                "image_url": result_path.replace("static", "/static")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"添加水印失败: {str(e)}"
        )


@router.post("/advanced/translate")
async def translate_text(
    text: str,
    from_lang: str = Form("zh"),
    to_lang: str = Form("en"),
    current_user = Depends(lambda: None)
):
    """
    翻译文字
    """
    try:
        result = await translation_service.translate_text(
            text,
            from_lang,
            to_lang
        )

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"翻译失败: {str(e)}"
        )


@router.post("/advanced/translate-ocr")
async def translate_ocr(
    file: UploadFile = File(...),
    from_lang: str = Form("zh"),
    to_lang: str = Form("en"),
    current_user = Depends(lambda: None)
):
    """
    翻译OCR结果
    """
    try:
        from app.services.ocr_service import OCRService

        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        # OCR识别
        ocr_service = OCRService()
        ocr_result = await ocr_service.ocr_image(temp_path, from_lang)

        # 翻译
        translated_result = await translation_service.translate_ocr_result(
            ocr_result,
            from_lang,
            to_lang
        )

        # 删除临时文件
        os.unlink(temp_path)

        return {
            "success": True,
            "data": translated_result
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"翻译OCR结果失败: {str(e)}"
        )


@router.post("/advanced/export-word")
async def export_word(
    text: str,
    title: str = Form("文档"),
    current_user = Depends(lambda: None)
):
    """
    导出为Word
    """
    try:
        output_path = office_service.export_to_word(text, title=title)

        return {
            "success": True,
            "data": {
                "word_url": output_path.replace("static", "/static")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Word导出失败: {str(e)}"
        )


@router.post("/advanced/export-excel")
async def export_excel(
    texts: list,
    sheet_name: str = Form("Sheet1"),
    current_user = Depends(lambda: None)
):
    """
    导出为Excel
    """
    try:
        output_path = office_service.export_to_excel(texts, sheet_name=sheet_name)

        return {
            "success": True,
            "data": {
                "excel_url": output_path.replace("static", "/static")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Excel导出失败: {str(e)}"
        )


@router.post("/advanced/create-long-image")
async def create_long_image(
    files: list[UploadFile] = File(...),
    spacing: int = Form(20),
    current_user = Depends(lambda: None)
):
    """
    创建长图片
    """
    try:
        # 保存所有文件
        image_paths = []
        for file in files:
            temp_path = await image_service.save_upload_file(file)
            image_paths.append(temp_path)

        # 创建长图片
        result_path = long_image_service.create_long_image(
            image_paths,
            spacing=spacing
        )

        # 删除临时文件
        for path in image_paths:
            os.unlink(path)

        return {
            "success": True,
            "data": {
                "image_url": result_path.replace("static", "/static")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"长图片创建失败: {str(e)}"
        )


@router.post("/advanced/create-grid-image")
async def create_grid_image(
    files: list[UploadFile] = File(...),
    columns: int = Form(2),
    spacing: int = Form(10),
    current_user = Depends(lambda: None)
):
    """
    创建网格图片
    """
    try:
        # 保存所有文件
        image_paths = []
        for file in files:
            temp_path = await image_service.save_upload_file(file)
            image_paths.append(temp_path)

        # 创建网格图片
        result_path = long_image_service.create_grid_image(
            image_paths,
            columns=columns,
            spacing=spacing
        )

        # 删除临时文件
        for path in image_paths:
            os.unlink(path)

        return {
            "success": True,
            "data": {
                "image_url": result_path.replace("static", "/static")
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"网格图片创建失败: {str(e)}"
        )
