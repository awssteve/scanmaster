"""
单元测试 - 图像处理服务
"""
import pytest
import asyncio
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path
from app.services.image_service import ImageService
import numpy as np
from PIL import Image


@pytest.fixture
def image_service():
    """图像处理服务fixture"""
    return ImageService()


@pytest.fixture
def test_image_path(tmp_path):
    """创建测试图片路径"""
    # 创建一个简单的测试图片
    img = Image.new('RGB', (100, 100), color='red')
    image_path = tmp_path / "test.jpg"
    img.save(image_path)
    return str(image_path)


@pytest.mark.asyncio
async def test_save_upload_file(image_service, tmp_path):
    """测试保存上传文件"""
    # 创建一个模拟文件
    from fastapi import UploadFile
    import io

    # 创建模拟文件
    file_content = b"test file content"
    file = UploadFile(filename="test.jpg", file=io.BytesIO(file_content))

    # 保存文件
    result_path = await image_service.save_upload_file(file)

    # 验证文件已保存
    assert Path(result_path).exists()
    assert result_path.endswith(".jpg")
    assert Path(result_path).parent == image_service.temp_dir


@pytest.mark.asyncio
async def test_enhance_image(image_service, test_image_path):
    """测试图像增强"""
    # 模拟OpenCV读取图片
    with patch('cv2.imread') as mock_imread, \
         patch('cv2.imwrite') as mock_imwrite:
        mock_imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)

        # 调用增强
        result_path = await image_service.enhance_image(test_image_path)

        # 验证文件路径
        assert result_path is not None
        assert "_enhanced" in result_path


@pytest.mark.asyncio
async def test_auto_crop(image_service, test_image_path):
    """测试自动裁剪"""
    # 模拟OpenCV操作
    with patch('cv2.imread') as mock_imread, \
         patch('cv2.Canny') as mock_canny, \
         patch('cv2.findContours') as mock_find_contours:
        # 模拟读取图片
        mock_imread.return_value = np.zeros((100, 100, 3), dtype=np.uint8)
        # 模拟边缘检测
        mock_canny.return_value = np.zeros((100, 100), dtype=np.uint8)
        # 模拟查找轮廓
        mock_find_contours.return_value = ([], None)

        # 调用裁剪
        result_path = await image_service.auto_crop(test_image_path)

        # 验证结果
        assert result_path is not None


@pytest.mark.asyncio
async def test_resize_image(image_service, test_image_path):
    """测试调整图片大小"""
    with patch('cv2.imwrite') as mock_imwrite:
        # 调用调整大小
        result_path = await image_service.resize_image(test_image_path, max_size=1920)

        # 验证结果
        assert result_path is not None


@pytest.mark.asyncio
async def test_process_document(image_service, test_image_path):
    """测试完整文档处理"""
    with patch('cv2.imwrite') as mock_imwrite:
        # 调用完整处理
        result_path = await image_service.process_document(
            test_image_path,
            enhance=True,
            auto_crop=True
        )

        # 验证结果
        assert result_path is not None
        # 注意：由于mock了cv2.imwrite，实际上不会创建新文件
        # 在实际测试中应该有真实的文件操作


@pytest.mark.asyncio
async def test_error_handling(image_service):
    """测试错误处理"""
    # 测试处理不存在的图片
    with pytest.raises(Exception):
        await image_service.enhance_image("/nonexistent/image.jpg")


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
