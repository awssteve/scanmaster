"""
PDF服务
"""
import logging
import os
from pathlib import Path
from typing import List
from PIL import Image
from PyPDF2 import PdfWriter
import uuid

logger = logging.getLogger(__name__)


class PDFService:
    """PDF服务"""

    def __init__(self):
        """初始化PDF服务"""
        self.output_dir = Path("static/pdfs")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    async def create_pdf(self, image_paths: List[str], filename: str = None) -> str:
        """
        创建PDF（从图片）

        Args:
            image_paths: 图片路径列表
            filename: 输出文件名

        Returns:
            PDF文件路径
        """
        try:
            # 生成文件名
            if filename is None:
                filename = f"document_{uuid.uuid4()}.pdf"

            pdf_path = self.output_dir / filename

            # 创建PDF
            pdf_writer = PdfWriter()

            # 添加每一页
            for image_path in image_paths:
                # 读取图片
                image = Image.open(image_path)

                # 转换为RGB
                if image.mode != 'RGB':
                    image = image.convert('RGB')

                # 添加到PDF
                image.save(
                    str(pdf_path),
                    "PDF",
                    resolution=100.0,
                    save_all=True,
                    append=False
                )

            logger.info(f"PDF创建成功: {pdf_path}")
            return f"/static/pdfs/{filename}"

        except Exception as e:
            logger.error(f"PDF创建失败: {e}")
            raise Exception(f"PDF创建失败: {str(e)}")

    async def merge_pdfs(self, pdf_paths: List[str], output_filename: str) -> str:
        """
        合并多个PDF

        Args:
            pdf_paths: PDF路径列表
            output_filename: 输出文件名

        Returns:
            合并后的PDF路径
        """
        try:
            output_path = self.output_dir / output_filename
            pdf_writer = PdfWriter()

            # 读取所有PDF
            for pdf_path in pdf_paths:
                from PyPDF2 import PdfReader
                reader = PdfReader(pdf_path)

                # 添加所有页面
                for page in reader.pages:
                    pdf_writer.add_page(page)

            # 保存
            with open(output_path, "wb") as output_file:
                pdf_writer.write(output_file)

            logger.info(f"PDF合并成功: {output_path}")
            return f"/static/pdfs/{output_filename}"

        except Exception as e:
            logger.error(f"PDF合并失败: {e}")
            raise Exception(f"PDF合并失败: {str(e)}")
