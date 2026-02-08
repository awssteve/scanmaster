"""
数据库模型
"""
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


def generate_uuid():
    """生成UUID"""
    return str(uuid.uuid4())


class User(Base):
    """用户表"""
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class Document(Base):
    """文档表"""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50), nullable=False)  # scan/id_card/passport/等
    file_path = Column(String(500), nullable=False)
    thumbnail_path = Column(String(500))
    ocr_result = Column(JSON)  # OCR识别结果
    metadata = Column(JSON)  # 元数据（文件大小、分辨率等）
    status = Column(String(20), default="processing")  # processing/success/failed
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class ScanHistory(Base):
    """扫描历史表"""
    __tablename__ = "scan_history"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    document_id = Column(String, nullable=False, index=True)
    operation = Column(String(50), nullable=False)  # scan/crop/enhance/ocr/export
    params = Column(JSON)  # 操作参数
    result = Column(JSON)  # 操作结果
    duration_ms = Column(Integer)  # 耗时（毫秒）
    created_at = Column(DateTime, server_default=func.now())


class IDCard(Base):
    """身份证信息表"""
    __tablename__ = "id_cards"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, index=True)
    document_id = Column(String, nullable=False, index=True)
    card_type = Column(String(20), nullable=False)  # id_card/passport/license/等
    name = Column(String(100))
    id_number = Column(String(100))
    address = Column(Text)
    phone = Column(String(20))
    issue_date = Column(String(20))
    expiry_date = Column(String(20))
    raw_data = Column(JSON)  # 原始OCR数据
    created_at = Column(DateTime, server_default=func.now())


class Setting(Base):
    """用户设置表"""
    __tablename__ = "settings"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, nullable=False, unique=True, index=True)
    settings = Column(JSON, nullable=False, default={})  # 设置JSON
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
