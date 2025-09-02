from typing import Any, Dict

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.core.dependencies import get_current_user, get_user_permissions
from app.models.user import User
from config.database import get_db
from app.crud import userdao
from app.core.security import verify_password, create_access_token
from app.schemas.common import APIResponse
from app.schemas.usercheck import LoginRequest
from app.core.exceptions import BusinessException
from config.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.models.user import User as DBUser

router = APIRouter(tags=["auth"])

@router.post("/token", response_model=APIResponse)
def login_access_token(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """获取访问令牌（JSON格式入参）"""
    # 验证用户
    user = userdao.get_user_by_username(db, username=login_data.username)
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise BusinessException(msg="用户名或密码错误", code=401)
    
    # 生成令牌
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        user.id, expires_delta=access_token_expires
    )
    return APIResponse(
        data={
	        "login_type": "account",
	        "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "username": user.username,
            "role": user.role
        }
    )
@router.post("/currentUser", response_model=APIResponse)
def read_users_me(
	db: Session = Depends(get_db),
	current_user: DBUser = Depends(get_current_user)
):
    """获取当前登录用户信息"""
    permissions = get_user_permissions(db, current_user)
    return APIResponse(
	    data={
        "userid": current_user.id,
        "name": current_user.username,
		"avatar": current_user.avatar,
        "email": current_user.email,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "permissions": permissions
    })