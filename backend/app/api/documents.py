"""
API路由 - 文档管理
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import os

from app.database import get_db
from app.models import Document
from app.services.ocr_service import OCRService
from app.services.image_service import ImageService

router = APIRouter()
ocr_service = OCRService()
image_service = ImageService()


@router.get("/documents", response_model=List[dict])
async def get_documents(user_id: str = "default", db: Session = Depends(get_db)):
    """获取文档列表"""
    documents = db.query(Document).filter(
        Document.user_id == user_id
    ).order_by(Document.created_at.desc()).all()

    return [
        {
            "id": doc.id,
            "name": doc.name,
            "type": doc.type,
            "created_at": doc.created_at.isoformat() if doc.created_at else None,
            "status": doc.status
        }
        for doc in documents
    ]


@router.get("/documents/{document_id}", response_model=dict)
async def get_document(document_id: str, user_id: str = "default", db: Session = Depends(get_db)):
    """获取文档详情"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )

    result = {
        "id": document.id,
        "name": document.name,
        "type": document.type,
        "created_at": document.created_at.isoformat() if document.created_at else None,
        "status": document.status,
        "metadata": document.metadata,
        "text": ""
    }

    # 提取OCR文字
    if document.ocr_result:
        result["text"] = document.ocr_result.get("text", "")
        result["textCount"] = document.ocr_result.get("count", 0)

    # 添加图片URL
    if document.file_path:
        result["image_url"] = document.file_path.replace("static", "/static")

    return result


@router.delete("/documents/{document_id}", response_model=dict)
async def delete_document(document_id: str, user_id: str = "default", db: Session = Depends(get_db)):
    """删除文档"""
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == user_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文档不存在"
        )

    # 删除文件
    if document.file_path and os.path.exists(document.file_path):
        os.unlink(document.file_path)

    if document.thumbnail_path and os.path.exists(document.thumbnail_path):
        os.unlink(document.thumbnail_path)

    # 删除数据库记录
    db.delete(document)
    db.commit()

    return {"success": True, "message": "文档已删除"}


@router.get("/history", response_model=List[dict])
async def get_scan_history(user_id: str = "default", db: Session = Depends(get_db)):
    """获取扫描历史"""
    from app.models import ScanHistory

    history = db.query(ScanHistory).filter(
        ScanHistory.user_id == user_id
    ).order_by(ScanHistory.created_at.desc()).limit(50).all()

    return [
        {
            "id": h.id,
            "name": h.operation,
            "timestamp": h.created_at.isoformat() if h.created_at else None,
            "textCount": h.result.get("count", 0) if h.result else 0
        }
        for h in history
    ]
