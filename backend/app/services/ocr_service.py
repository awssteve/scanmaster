"""
OCR服务 - 基于PaddleOCR
"""
import logging
from typing import Dict, Any, List
from paddleocr import PaddleOCR
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)


class OCRService:
    """OCR服务"""

    def __init__(self):
        """初始化OCR服务"""
        self.ocr_ch = None  # 中文OCR
        self.ocr_en = None  # 英文OCR
        self.ocr_ch_en = None  # 中英文OCR
        self._ready = False

    def is_ready(self) -> bool:
        """检查OCR服务是否就绪"""
        return self._ready

    def _init_ocr(self, lang: str):
        """初始化指定语言的OCR模型"""
        logger.info(f"初始化OCR模型: {lang}")

        try:
            if lang == "ch":
                # 中文OCR
                ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang="ch",
                    use_gpu=True,
                    show_log=False
                )
            elif lang == "en":
                # 英文OCR
                ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang="en",
                    use_gpu=True,
                    show_log=False
                )
            else:  # ch_en
                # 中英文OCR
                ocr = PaddleOCR(
                    use_angle_cls=True,
                    lang="ch",
                    use_gpu=True,
                    show_log=False
                )

            logger.info(f"OCR模型初始化成功: {lang}")
            return ocr

        except Exception as e:
            logger.error(f"OCR模型初始化失败: {e}")
            return None

    def _get_ocr_model(self, lang: str):
        """获取OCR模型（懒加载）"""
        if lang == "ch":
            if self.ocr_ch is None:
                self.ocr_ch = self._init_ocr("ch")
            return self.ocr_ch
        elif lang == "en":
            if self.ocr_en is None:
                self.ocr_en = self._init_ocr("en")
            return self.ocr_en
        else:  # ch_en
            if self.ocr_ch_en is None:
                self.ocr_ch_en = self._init_ocr("ch_en")
            return self.ocr_ch_en

    async def ocr_image(self, image_path: str, lang: str = "ch") -> Dict[str, Any]:
        """
        OCR文字识别

        Args:
            image_path: 图片路径
            lang: 语言类型 (ch/en/ch_en)

        Returns:
            OCR识别结果
        """
        try:
            # 懒加载模型
            ocr = self._get_ocr_model(lang)
            if ocr is None:
                raise Exception("OCR模型初始化失败")

            # 读取图片
            image = np.array(Image.open(image_path))

            # OCR识别
            result = ocr.ocr(image, cls=True)

            # 解析结果
            texts = []
            positions = []

            if result and result[0]:
                for line in result[0]:
                    # 提取文本
                    text = line[1][0]
                    texts.append(text)

                    # 提取位置
                    position = line[0]
                    positions.append(position)

            self._ready = True

            return {
                "text": "\n".join(texts),
                "texts": texts,
                "positions": positions,
                "count": len(texts)
            }

        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            raise Exception(f"OCR识别失败: {str(e)}")

    async def ocr_batch(self, image_paths: List[str], lang: str = "ch") -> List[Dict[str, Any]]:
        """
        批量OCR识别

        Args:
            image_paths: 图片路径列表
            lang: 语言类型

        Returns:
            OCR识别结果列表
        """
        results = []
        for image_path in image_paths:
            result = await self.ocr_image(image_path, lang)
            results.append(result)
        return results
