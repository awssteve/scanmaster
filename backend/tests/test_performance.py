"""
性能测试 - OCR服务
"""
import pytest
import asyncio
import time
from app.services.ocr_service import OCRService
from pathlib import Path
import numpy as np
from PIL import Image


@pytest.fixture
def ocr_service():
    """OCR服务fixture"""
    return OCRService()


@pytest.fixture
def test_image(tmp_path):
    """创建性能测试用图片"""
    # 创建一个1000x1000的测试图片
    img = Image.new('RGB', (1000, 1000), color='white')
    draw = Image.new('RGB', (1000, 1000), color='black')

    # 添加一些文字（简化）
    from PIL import ImageDraw
    draw = ImageDraw.Draw(draw)
    draw.text((100, 100), "测试文字", fill='white')

    # 合并
    img.paste(draw, (0, 0))

    # 保存
    image_path = tmp_path / "performance_test.jpg"
    img.save(image_path)
    return str(image_path)


@pytest.mark.asyncio
@pytest.mark.slow
async def test_ocr_performance(ocr_service, test_image):
    """测试OCR性能"""
    # 模拟初始化
    ocr_service.ocr_ch = None

    # Mock PaddleOCR
    class MockOCR:
        def ocr(self, img, cls=True):
            start_time = time.time()
            # 模拟OCR处理时间（100ms）
            time.sleep(0.1)
            end_time = time.time()
            return [[["测试文字"], [[0,0], [100,0], [100,30], [0,30]]]]

    ocr_service._get_ocr_model = lambda lang: MockOCR()

    # 执行OCR
    start_time = time.time()
    result = await ocr_service.ocr_image(test_image, "ch")
    end_time = time.time()

    # 验证结果
    assert result is not None
    assert result["text"] == "测试文字"
    assert result["count"] == 1

    # 验证性能（应该在200ms以内）
    execution_time = end_time - start_time
    print(f"OCR执行时间: {execution_time:.2f}秒")
    assert execution_time < 0.2, f"OCR执行时间过长: {execution_time:.2f}秒"


@pytest.mark.asyncio
@pytest.mark.slow
async def test_batch_ocr_performance(ocr_service, tmp_path):
    """测试批量OCR性能"""
    # 创建10个测试图片
    test_images = []
    for i in range(10):
        img = Image.new('RGB', (500, 500), color='white')
        image_path = tmp_path / f"test_{i}.jpg"
        img.save(image_path)
        test_images.append(str(image_path))

    # Mock PaddleOCR
    class MockOCR:
        def ocr(self, img, cls=True):
            time.sleep(0.05)  # 模拟50ms处理时间
            return [[["测试"], [[0,0], [100,0], [100,30], [0,30]]]]

    ocr_service._get_ocr_model = lambda lang: MockOCR()

    # 执行批量OCR
    start_time = time.time()
    results = await ocr_service.ocr_batch(test_images, "ch")
    end_time = time.time()

    # 验证结果
    assert len(results) == 10
    assert all(r["success"] for r in results)

    # 验证性能（10个图片应该在1秒以内完成，因为有并发）
    execution_time = end_time - start_time
    print(f"批量OCR执行时间: {execution_time:.2f}秒（10张图片）")
    assert execution_time < 1.0, f"批量OCR执行时间过长: {execution_time:.2f}秒"


if __name__ == '__main__':
    pytest.main([__file__, '-v', '-m', 'slow'])
