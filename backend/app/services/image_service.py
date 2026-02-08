"""
图像处理服务
"""
import logging
import os
import uuid
from pathlib import Path
from typing import List
import cv2
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
from fastapi import UploadFile
import aiofiles

logger = logging.getLogger(__name__)


class ImageService:
    """图像处理服务"""

    def __init__(self):
        """初始化图像处理服务"""
        self.upload_dir = Path("uploads")
        self.temp_dir = Path("temp")
        self.upload_dir.mkdir(exist_ok=True)
        self.temp_dir.mkdir(exist_ok=True)

    async def save_upload_file(self, file: UploadFile) -> str:
        """
        保存上传的文件

        Args:
            file: 上传的文件

        Returns:
            文件路径
        """
        # 生成唯一文件名
        file_extension = Path(file.filename).suffix
        unique_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = self.temp_dir / unique_filename

        # 保存文件
        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        logger.info(f"文件保存成功: {file_path}")
        return str(file_path)

    async def enhance_image(self, image_path: str) -> str:
        """
        图像增强（对比度、锐化、去噪）

        Args:
            image_path: 图片路径

        Returns:
            处理后的图片路径
        """
        try:
            # 读取图片
            image = Image.open(image_path)

            # 转换为RGB
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # 对比度增强
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.5)

            # 锐化
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)

            # 去噪
            image = image.filter(ImageFilter.MedianFilter(size=3))

            # 保存
            output_path = self.temp_dir / f"{uuid.uuid4()}_enhanced.jpg"
            image.save(output_path, "JPEG", quality=95)

            # 删除原文件
            os.unlink(image_path)

            logger.info(f"图像增强完成: {output_path}")
            return str(output_path)

        except Exception as e:
            logger.error(f"图像增强失败: {e}")
            raise Exception(f"图像增强失败: {str(e)}")

    async def auto_crop(self, image_path: str) -> str:
        """
        自动裁剪（检测文档边界）

        Args:
            image_path: 图片路径

        Returns:
            处理后的图片路径
        """
        try:
            # 读取图片
            image = cv2.imread(image_path)

            # 转为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 高斯模糊
            blurred = cv2.GaussianBlur(gray, (5, 5), 0)

            # 边缘检测
            edged = cv2.Canny(blurred, 75, 200)

            # 查找轮廓
            contours, _ = cv2.findContours(
                edged.copy(),
                cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE
            )

            # 找到最大轮廓（文档）
            if contours:
                c = max(contours, key=cv2.contourArea)

                # 多边形近似
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.02 * peri, True)

                # 如果是四边形
                if len(approx) == 4:
                    # 裁剪
                    pts = approx.reshape(4, 2)
                    rect = self._order_points(pts)
                    warped = self._four_point_transform(image, rect)

                    # 保存
                    output_path = self.temp_dir / f"{uuid.uuid4()}_cropped.jpg"
                    cv2.imwrite(str(output_path), warped)

                    # 删除原文件
                    os.unlink(image_path)

                    logger.info(f"自动裁剪完成: {output_path}")
                    return str(output_path)

            # 如果没有找到四边形，返回原图
            return image_path

        except Exception as e:
            logger.error(f"自动裁剪失败: {e}")
            # 失败返回原图
            return image_path

    def _order_points(self, pts):
        """对点进行排序"""
        rect = np.zeros((4, 2), dtype="float32")

        # 按x坐标排序
        s = pts.sum(axis=1)
        diff = np.diff(pts, axis=1)

        rect[0] = pts[np.argmin(s)]
        rect[2] = pts[np.argmax(s)]
        rect[1] = pts[np.argmin(diff)]
        rect[3] = pts[np.argmax(diff)]

        return rect

    def _four_point_transform(self, image, pts):
        """四点透视变换"""
        rect = self._order_points(pts)
        (tl, tr, br, bl) = rect

        # 计算宽度
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        # 计算高度
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        # 目标点
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]
        ], dtype="float32")

        # 透视变换矩阵
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped

    async def process_document(
        self,
        image_path: str,
        enhance: bool = True,
        auto_crop: bool = True
    ) -> str:
        """
        完整文档处理流程

        Args:
            image_path: 图片路径
            enhance: 是否增强
            auto_crop: 是否自动裁剪

        Returns:
            处理后的图片路径
        """
        processed_path = image_path

        if auto_crop:
            processed_path = await self.auto_crop(processed_path)

        if enhance:
            processed_path = await self.enhance_image(processed_path)

        return processed_path

    async def resize_image(self, image_path: str, max_size: int = 1920) -> str:
        """
        调整图片大小

        Args:
            image_path: 图片路径
            max_size: 最大尺寸

        Returns:
            处理后的图片路径
        """
        try:
            image = Image.open(image_path)

            # 调整大小
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)

            # 保存
            output_path = self.temp_dir / f"{uuid.uuid4()}_resized.jpg"
            image.save(output_path, "JPEG", quality=90)

            # 删除原文件
            os.unlink(image_path)

            return str(output_path)

        except Exception as e:
            logger.error(f"调整图片大小失败: {e}")
            return image_path
