"""
去水印服务
"""
import logging
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import cv2
from typing import Tuple

logger = logging.getLogger(__name__)


class WatermarkService:
    """去水印服务"""

    def __init__(self):
        pass

    def remove_text_watermark(
        self,
        image_path: str,
        watermark_text: str = None,
        position: Tuple[int, int] = None
    ) -> str:
        """
        去除文字水印

        Args:
            image_path: 图片路径
            watermark_text: 水印文字（可选，用于OCR识别）
            position: 水印位置（可选）

        Returns:
            去水印后的图片路径
        """
        try:
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                raise Exception("无法读取图片")

            # 如果知道水印位置，直接修补
            if position:
                # 使用inpaint算法修复
                h, w = image.shape[:2]
                x, y = position
                # 创建mask
                mask = np.zeros((h, w), np.uint8)
                # 假设水印区域（简化）
                mask[y:y+50, x:x+200] = 255
                # inpaint
                result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
            else:
                # 使用基于纹理的修复（简化版）
                # 实际需要更复杂的算法
                result = self._texture_based_removal(image)

            # 保存结果
            output_path = image_path.replace(".", "_no_watermark.")
            cv2.imwrite(output_path, result)

            logger.info(f"文字水印去除完成: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"去除文字水印失败: {e}")
            return image_path

    def remove_logo_watermark(
        self,
        image_path: str,
        logo_position: Tuple[int, int, int, int] = None
    ) -> str:
        """
        去除Logo水印

        Args:
            image_path: 图片路径
            logo_position: Logo位置 (x1, y1, x2, y2)

        Returns:
            去Logo后的图片路径
        """
        try:
            # 读取图片
            image = cv2.imread(image_path)
            if image is None:
                raise Exception("无法读取图片")

            # 如果知道Logo位置，直接修补
            if logo_position:
                x1, y1, x2, y2 = logo_position
                h, w = image.shape[:2]
                # 创建mask
                mask = np.zeros((h, w), np.uint8)
                mask[y1:y2, x1:x2] = 255
                # inpaint
                result = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)
            else:
                # 使用边缘检测+纹理修复（简化版）
                result = self._logo_based_removal(image)

            # 保存结果
            output_path = image_path.replace(".", "_no_logo.")
            cv2.imwrite(output_path, result)

            logger.info(f"Logo水印去除完成: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"去除Logo水印失败: {e}")
            return image_path

    def _texture_based_removal(self, image: np.ndarray) -> np.ndarray:
        """基于纹理的去除（简化版）"""
        # 实际需要更复杂的算法
        # 这里只是示例

        # 高斯模糊
        blurred = cv2.GaussianBlur(image, (5, 5), 0)

        # 边缘检测
        edges = cv2.Canny(blurred, 50, 150)

        # 找到可能的文字区域
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # 过滤小轮廓
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100 and area < 5000:
                # 可能是文字，修复
                x, y, w, h = cv2.boundingRect(contour)
                mask = np.zeros(image.shape[:2], np.uint8)
                cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
                image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

        return image

    def _logo_based_removal(self, image: np.ndarray) -> np.ndarray:
        """基于Logo的去除（简化版）"""
        # 实际需要更复杂的算法
        # 这里只是示例

        # 转为灰度
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # 边缘检测
        edges = cv2.Canny(gray, 30, 100)

        # 查找轮廓
        contours, _ = cv2.findContours(
            edges,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        # 找到可能是Logo的轮廓（较大、规则形状）
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 10000:
                # 可能是Logo
                x, y, w, h = cv2.boundingRect(contour)
                mask = np.zeros(image.shape[:2], np.uint8)
                cv2.rectangle(mask, (x, y), (x+w, y+h), 255, -1)
                image = cv2.inpaint(image, mask, 3, cv2.INPAINT_TELEA)

        return image

    def add_watermark(
        self,
        image_path: str,
        watermark_text: str = "智扫通",
        position: str = "bottom_right",
        opacity: float = 0.3
    ) -> str:
        """
        添加水印

        Args:
            image_path: 图片路径
            watermark_text: 水印文字
            position: 位置 (top_left, top_right, bottom_left, bottom_right, center)
            opacity: 透明度 (0-1)

        Returns:
            添加水印后的图片路径
        """
        try:
            # 打开图片
            image = Image.open(image_path).convert('RGBA')

            # 创建水印
            txt = Image.new('RGBA', image.size, (255, 255, 255, 0))

            # 设置字体（简化版，使用默认字体）
            font_size = int(image.size[0] / 30)
            draw = ImageDraw.Draw(txt)

            # 计算位置
            text_bbox = draw.textbbox((0, 0), watermark_text)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]

            if position == "top_left":
                x, y = 10, 10
            elif position == "top_right":
                x, y = image.size[0] - text_width - 10, 10
            elif position == "bottom_left":
                x, y = 10, image.size[1] - text_height - 10
            elif position == "bottom_right":
                x, y = image.size[0] - text_width - 10, image.size[1] - text_height - 10
            else:  # center
                x, y = (image.size[0] - text_width) // 2, (image.size[1] - text_height) // 2

            # 绘制文字（带透明度）
            watermark_color = (255, 255, 255, int(255 * opacity))
            draw.text((x, y), watermark_text, fill=watermark_color)

            # 合成
            watermarked = Image.alpha_composite(image, txt)

            # 转换回RGB
            watermarked = watermarked.convert('RGB')

            # 保存
            output_path = image_path.replace(".", "_watermarked.")
            watermarked.save(output_path, 'JPEG', quality=95)

            logger.info(f"水印添加完成: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"添加水印失败: {e}")
            return image_path
