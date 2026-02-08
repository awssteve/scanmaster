"""
单元测试 - OCR服务
"""
import pytest
import asyncio
from unittest.mock import Mock, patch
from app.services.ocr_service import OCRService


@pytest.fixture
def ocr_service():
    """OCR服务fixture"""
    return OCRService()


@pytest.mark.asyncio
async def test_ocr_service_initialization(ocr_service):
    """测试OCR服务初始化"""
    # 测试服务是否可以正常实例化
    assert ocr_service is not None
    assert hasattr(ocr_service, 'ocr_ch')
    assert hasattr(ocr_service, 'ocr_en')
    assert hasattr(ocr_service, 'ocr_ch_en')


@pytest.mark.asyncio
async def test_ocr_image_chinese(ocr_service):
    """测试中文OCR"""
    # 模拟OCR结果
    mock_result = {
        "text": "测试文字",
        "texts": ["测试文字"],
        "positions": [[[0,0], [100,0], [100,30], [0,30]]],
        "count": 1
    }

    # 模拟PaddleOCR
    with patch.object(ocr_service, '_get_ocr_model') as mock_get_model:
        mock_ocr = Mock()
        mock_ocr.ocr = Mock(return_value=[[mock_result["texts"]], mock_result["positions"]]])
        mock_get_model.return_value = mock_ocr

        # 调用OCR
        result = await ocr_service.ocr_image("test.jpg", "ch")

        # 验证结果
        assert result is not None
        assert result["text"] == "测试文字"
        assert result["count"] == 1


@pytest.mark.asyncio
async def test_ocr_batch(ocr_service):
    """测试批量OCR"""
    mock_result = {
        "text": "测试",
        "texts": ["测试"],
        "positions": [],
        "count": 1
    }

    with patch.object(ocr_service, 'ocr_image', return_value=mock_result):
        results = await ocr_service.ocr_batch(["test1.jpg", "test2.jpg"], "ch")

        # 验证结果
        assert len(results) == 2
        assert all(r["success"] for r in results)


@pytest.mark.asyncio
async def test_ocr_service_error_handling(ocr_service):
    """测试OCR服务错误处理"""
    # 模拟PaddleOCR抛出异常
    with patch.object(ocr_service, '_get_ocr_model', side_effect=Exception("OCR failed")):
        with pytest.raises(Exception) as exc_info:
            await ocr_service.ocr_image("test.jpg", "ch")

        # 验证异常
        assert str(exc_info.value) == "OCR识别失败: OCR failed"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
