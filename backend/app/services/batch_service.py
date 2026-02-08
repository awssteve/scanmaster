"""
批量处理服务
"""
import logging
import asyncio
from typing import List
from pathlib import Path
from app.services.ocr_service import OCRService
from app.services.image_service import ImageService
from app.services.pdf_service import PDFService

logger = logging.getLogger(__name__)


class BatchService:
    """批量处理服务"""

    def __init__(self):
        self.ocr_service = OCRService()
        self.image_service = ImageService()
        self.pdf_service = PDFService()

    async def batch_ocr(self, image_paths: List[str], lang: str = "ch") -> List[dict]:
        """
        批量OCR识别

        Args:
            image_paths: 图片路径列表
            lang: 语言类型

        Returns:
            OCR识别结果列表
        """
        tasks = []
        for path in image_paths:
            task = self.ocr_service.ocr_image(path, lang)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 处理异常
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"图片{i+1} OCR失败: {result}")
                processed_results.append({
                    "success": False,
                    "image": image_paths[i],
                    "error": str(result)
                })
            else:
                processed_results.append({
                    "success": True,
                    "image": image_paths[i],
                    "result": result
                })

        return processed_results

    async def batch_enhance(self, image_paths: List[str]) -> List[str]:
        """
        批量图像增强

        Args:
            image_paths: 图片路径列表

        Returns:
            增强后的图片路径列表
        """
        tasks = []
        for path in image_paths:
            task = self.image_service.enhance_image(path)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"图片{i+1}增强失败: {result}")
                processed_results.append(image_paths[i])
            else:
                processed_results.append(result)

        return processed_results

    async def batch_crop(self, image_paths: List[str]) -> List[str]:
        """
        批量自动裁剪

        Args:
            image_paths: 图片路径列表

        Returns:
            裁剪后的图片路径列表
        """
        tasks = []
        for path in image_paths:
            task = self.image_service.auto_crop(path)
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"图片{i+1}裁剪失败: {result}")
                processed_results.append(image_paths[i])
            else:
                processed_results.append(result)

        return processed_results

    async def batch_pdf_export(
        self,
        image_paths: List[str],
        output_filename: str = None
    ) -> str:
        """
        批量导出为单个PDF

        Args:
            image_paths: 图片路径列表
            output_filename: 输出文件名

        Returns:
            PDF文件路径
        """
        if output_filename is None:
            output_filename = f"batch_{uuid.uuid4().hex}.pdf"

        pdf_path = await self.pdf_service.create_pdf(image_paths, output_filename)
        return pdf_path
