"""
长图片合成服务
"""
import logging
from pathlib import Path
from typing import List
from PIL import Image
import io

logger = logging.getLogger(__name__)


class LongImageService:
    """长图片合成服务"""

    def __init__(self):
        pass

    def create_long_image(
        self,
        image_paths: List[str],
        output_path: str = None,
        spacing: int = 20,
        background_color: tuple = (255, 255, 255, 0)
    ) -> str:
        """
        创建长图片

        Args:
            image_paths: 图片路径列表
            output_path: 输出文件路径
            spacing: 图片间距（像素）
            background_color: 背景颜色

        Returns:
            长图片路径
        """
        try:
            # 打开所有图片
            images = []
            max_width = 0
            total_height = 0

            for img_path in image_paths:
                img = Image.open(img_path)

                # 转换为RGBA
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                images.append(img)

                # 记录最大宽度
                if img.size[0] > max_width:
                    max_width = img.size[0]

                # 累加高度
                total_height += img.size[1]

            # 添加间距
            if len(images) > 1:
                total_height += spacing * (len(images) - 1)

            # 创建画布
            canvas = Image.new(
                'RGBA',
                (max_width, total_height),
                background_color
            )

            # 拼接图片
            y_offset = 0
            for i, img in enumerate(images):
                # 居中对齐
                x_offset = (max_width - img.size[0]) // 2

                # 粘贴图片
                canvas.paste(img, (x_offset, y_offset), img)

                # 移动y偏移
                y_offset += img.size[1]

                # 添加间距（除了最后一张）
                if i < len(images) - 1:
                    y_offset += spacing

            # 保存
            if output_path is None:
                output_path = f"long_image_{timestamp()}.png"

            # 如果背景是透明的，保存为PNG
            if background_color[3] == 0:
                canvas.save(output_path, 'PNG')
            else:
                # 否则转换为RGB保存为JPEG
                canvas_rgb = canvas.convert('RGB')
                canvas_rgb.save(output_path, 'JPEG', quality=95)

            logger.info(f"长图片合成成功: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"长图片合成失败: {e}")
            raise Exception(f"长图片合成失败: {str(e)}")

    def create_grid_image(
        self,
        image_paths: List[str],
        output_path: str = None,
        columns: int = 2,
        spacing: int = 10,
        background_color: tuple = (255, 255, 255, 0)
    ) -> str:
        """
        创建网格图片

        Args:
            image_paths: 图片路径列表
            output_path: 输出文件路径
            columns: 列数
            spacing: 间距（像素）
            background_color: 背景颜色

        Returns:
            网格图片路径
        """
        try:
            # 打开所有图片
            images = []
            max_width = 0
            max_height = 0

            for img_path in image_paths:
                img = Image.open(img_path)

                # 转换为RGBA
                if img.mode != 'RGBA':
                    img = img.convert('RGBA')

                images.append(img)

                # 记录最大尺寸
                if img.size[0] > max_width:
                    max_width = img.size[0]
                if img.size[1] > max_height:
                    max_height = img.size[1]

            # 计算行列
            rows = (len(images) + columns - 1) // columns

            # 计算画布大小
            canvas_width = max_width * columns + spacing * (columns - 1)
            canvas_height = max_height * rows + spacing * (rows - 1)

            # 创建画布
            canvas = Image.new(
                'RGBA',
                (canvas_width, canvas_height),
                background_color
            )

            # 拼接图片
            for i, img in enumerate(images):
                # 计算行列位置
                row = i // columns
                col = i % columns

                # 计算坐标
                x = col * (max_width + spacing)
                y = row * (max_height + spacing)

                # 居中放置
                x_offset = x + (max_width - img.size[0]) // 2
                y_offset = y + (max_height - img.size[1]) // 2

                # 粘贴图片
                canvas.paste(img, (x_offset, y_offset), img)

            # 保存
            if output_path is None:
                output_path = f"grid_image_{timestamp()}.png"

            # 如果背景是透明的，保存为PNG
            if background_color[3] == 0:
                canvas.save(output_path, 'PNG')
            else:
                # 否则转换为RGB保存为JPEG
                canvas_rgb = canvas.convert('RGB')
                canvas_rgb.save(output_path, 'JPEG', quality=95)

            logger.info(f"网格图片合成成功: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"网格图片合成失败: {e}")
            raise Exception(f"网格图片合成失败: {str(e)}")


def timestamp():
    """生成时间戳"""
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d_%H%M%S")
