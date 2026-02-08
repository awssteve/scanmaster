"""
API路由 - 用户认证
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import User
from app.services.auth_service import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    get_current_user
)

router = APIRouter()


@router.post("/auth/register")
async def register(
    username: str,
    email: str,
    password: str,
    db: Session = Depends(get_db)
):
    """
    用户注册
    """
    # 检查用户名是否存在
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否存在
    existing_email = db.query(User).filter(User.email == email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )

    # 创建用户
    user = User(
        id=str(uuid.uuid4()),
        username=username,
        email=email,
        password_hash=get_password_hash(password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "success": True,
        "message": "注册成功",
        "data": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }


@router.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录
    """
    # 查找用户
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 验证密码
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )

    # 创建令牌
    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})

    return {
        "success": True,
        "data": {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }
    }


@router.get("/auth/me")
async def get_me(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息
    """
    return {
        "success": True,
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "email": current_user.email,
            "created_at": current_user.created_at.isoformat() if current_user.created_at else None
        }
    }


@router.post("/auth/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """
    刷新令牌
    """
    try:
        from app.services.auth_service import decode_token

        payload = decode_token(refresh_token)

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="令牌类型错误"
            )

        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的令牌"
            )

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="用户不存在"
            )

        # 创建新令牌
        access_token = create_access_token(data={"sub": user.id})
        new_refresh_token = create_refresh_token(data={"sub": user.id})

        return {
            "success": True,
            "data": {
                "access_token": access_token,
                "refresh_token": new_refresh_token
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="刷新令牌失败"
        )
