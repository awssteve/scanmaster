"""
智扫通后端服务 - FastAPI应用（完整版）
"""
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import logging
import os
from pathlib import Path

from app.core.config import settings
from app.database import init_db
from app.api import documents, id_card, auth, batch, advanced
from app.services.ocr_service import OCRService
from app.services.pdf_service import PDFService
from app.services.image_service import ImageService

# 配置日志
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="智扫通API",
    description="智能文档扫描工具后端API",
    version="1.0.0"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化服务
ocr_service = OCRService()
pdf_service = PDFService()
image_service = ImageService()

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 确保必要的目录存在
os.makedirs("static", exist_ok=True)
os.makedirs("static/pdfs", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("temp", exist_ok=True)

# 注册路由
app.include_router(documents.router, prefix="/api/v1", tags=["文档"])
app.include_router(id_card.router, prefix="/api/v1", tags=["证件"])
app.include_router(auth.router, prefix="/api/v1", tags=["认证"])
app.include_router(batch.router, prefix="/api/v1", tags=["批量处理"])
app.include_router(advanced.router, prefix="/api/v1", tags=["高级功能"])


@app.on_event("startup")
async def startup_event():
    """启动事件"""
    logger.info("智扫通API启动中...")
    init_db()
    logger.info("智扫通API启动完成")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用智扫通API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "ocr_ready": ocr_service.is_ready()
    }


@app.post("/api/v1/ocr")
async def ocr_image(
    file: UploadFile = File(...),
    lang: str = Form("ch")  # ch: 中文, en: 英文, ch_en: 中英文
):
    """
    OCR文字识别

    Args:
        file: 图片文件
        lang: 语言类型

    Returns:
        OCR识别结果
    """
    try:
        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        # OCR识别
        result = await ocr_service.ocr_image(temp_path, lang)

        # 删除临时文件
        os.unlink(temp_path)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        logger.error(f"OCR识别失败: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"OCR识别失败: {str(e)}"
            }
        )


@app.post("/api/v1/scan")
async def scan_document(
    file: UploadFile = File(...),
    enhance: bool = Form(True),  # 是否增强图像
    auto_crop: bool = Form(True)  # 是否自动裁剪
):
    """
    文档扫描（拍照扫描）

    Args:
        file: 图片文件
        enhance: 是否增强图像
        auto_crop: 是否自动裁剪

    Returns:
        扫描结果（图像+OCR）
    """
    try:
        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        # 图像处理
        processed_path = await image_service.process_document(
            temp_path,
            enhance=enhance,
            auto_crop=auto_crop
        )

        # OCR识别
        ocr_result = await ocr_service.ocr_image(processed_path, "ch")

        # 删除临时文件
        os.unlink(temp_path)

        return {
            "success": True,
            "data": {
                "image_url": processed_path.replace("static", "/static"),
                "ocr_result": ocr_result
            }
        }

    except Exception as e:
        logger.error(f"文档扫描失败: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"文档扫描失败: {str(e)}"
            }
        )


@app.post("/api/v1/pdf/export")
async def export_pdf(
    images: list[UploadFile] = File(...),
    filename: str = Form("document.pdf")
):
    """
    导出PDF

    Args:
        images: 图片文件列表
        filename: 输出文件名

    Returns:
        PDF文件
    """
    try:
        # 保存所有图片
        image_paths = []
        for image in images:
            temp_path = await image_service.save_upload_file(image)
            image_paths.append(temp_path)

        # 生成PDF
        pdf_path = await pdf_service.create_pdf(image_paths, filename)

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
        logger.error(f"PDF导出失败: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"PDF导出失败: {str(e)}"
            }
        )


@app.post("/api/v1/document/process")
async def process_document(
    file: UploadFile = File(...),
    operations: str = Form("enhance,crop,ocr")  # 处理操作
):
    """
    完整文档处理流程

    Args:
        file: 文档文件（图片/PDF）
        operations: 处理操作（逗号分隔）

    Returns:
        处理结果
    """
    try:
        # 解析操作
        ops = [op.strip() for op in operations.split(",")]

        # 保存临时文件
        temp_path = await image_service.save_upload_file(file)

        result = {}

        # 图像增强
        if "enhance" in ops:
            temp_path = await image_service.enhance_image(temp_path)
            result["enhanced"] = True

        # 自动裁剪
        if "crop" in ops:
            temp_path = await image_service.auto_crop(temp_path)
            result["cropped"] = True

        # OCR识别
        if "ocr" in ops:
            ocr_result = await ocr_service.ocr_image(temp_path, "ch")
            result["ocr"] = ocr_result

        # 删除临时文件
        os.unlink(temp_path)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        logger.error(f"文档处理失败: {e}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"文档处理失败: {str(e)}"
            }
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
