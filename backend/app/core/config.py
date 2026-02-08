"""
应用配置（完整版）
"""
from pydantic_settings import BaseSettings
from typing import List
from pathlib import Path


class Settings(BaseSettings):
    """应用配置"""

    # 项目信息
    PROJECT_NAME: str = "智扫通"
    VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"

    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "sqlite:///./scanmaster.db"

    # 文件上传
    MAX_UPLOAD_SIZE: int = 50 * 1024 * 1024  # 50MB
    ALLOWED_EXTENSIONS: list = [".jpg", ".jpeg", ".png", ".gif", ".webp", ".pdf"]

    # OCR配置
    OCR_LANG_DEFAULT: str = "ch"
    OCR_USE_GPU: bool = True

    # 目录配置
    BASE_DIR: Path = Path(__file__).parent.parent
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    TEMP_DIR: Path = BASE_DIR / "temp"
    STATIC_DIR: Path = BASE_DIR / "static"

    # CORS配置
    CORS_ORIGINS: List[str] = ["*"]

    # 日志配置
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
