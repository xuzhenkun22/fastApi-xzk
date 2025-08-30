from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud import userdao
from app.schemas.usercheck import User, UserCreate, UserUpdate
from config.database import get_db

router = APIRouter()

@router.get("/", response_model=List[User], summary="获取用户列表")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """：
    获取用户列表，支持分页：
    - skip: 跳过前面的用户数量，默认为0
    - limit: 最大返回数量，默认为100
    """
    users = userdao.get_users(db, skip=skip, limit=limit)
    return users

@router.get("/{user_id}", response_model=User, summary="获取单个用户")
def read_user(user_id: int, db: Session = Depends(get_db)):
    """根据用户ID获取用户详情"""
    db_user = userdao.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED, summary="创建新用户")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """创建新用户"""
    # 检查用户名是否已存在
    db_user = userdao.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )

    # 检查邮箱是否已存在
    db_user = userdao.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已存在"
        )

    return userdao.create_user(db=db, user=user)

@router.put("/{user_id}", response_model=User, summary="更新用户信息")
def update_user(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(get_db)
):
    """根据用户ID更新用户信息"""
    db_user = userdao.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    # 如果更新了用户名，检查新用户名是否已存在
    if user.username and user.username != db_user.username:
        existing_user = userdao.get_user_by_username(db, username=user.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已存在"
            )

    # 如果更新了邮箱，检查新邮箱是否已存在
    if user.email and user.email != db_user.email:
        existing_user = userdao.get_user_by_email(db, email=user.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已存在"
            )

    return userdao.update_user(db=db, db_user=db_user, user_update=user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除用户")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """根据用户ID删除用户"""
    success = userdao.delete_user(db, user_id=user_id)
    if not success:
        raise HTTPException(status_code=404, detail="用户不存在")
    return None
