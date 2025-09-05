from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.crud import userdao
from app.schemas.usercheck import (
    User, UserCreate, UserUpdate, 
    UserQuery, UserGet, UserDelete
)
from app.schemas.common import APIResponse
from config.database import get_db
from app.core.dependencies import get_current_user, is_admin
from app.core.exceptions import BusinessException
from app.models.user import User as DBUser

router = APIRouter()

@router.post("/list", response_model=APIResponse[List[User]], summary="获取用户列表")
def read_users(
    params: UserQuery,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(is_admin)
):
    """获取用户列表（分页）"""
    # 验证分页参数合理性
    if params.pageSize > 500:
        raise BusinessException(msg="每页最大记录数不能超过500", code=400)

    users = userdao.get_users(db, current=params.current, pageSize=params.pageSize)
    return APIResponse(data=users)

@router.post("/get", response_model=APIResponse[User], summary="获取单个用户")
def read_user(
    params: UserGet,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """获取用户详情（仅本人或管理员）"""
    db_user = userdao.get_user(db, user_id=params.user_id)
    if not db_user:
        raise BusinessException(msg="用户不存在", code=404)

    # 权限检查
    if db_user.id != current_user.id and current_user.role != "admin":
        raise BusinessException(msg="无权限访问", code=403)

    return APIResponse(data=db_user)

@router.post("/create", response_model=APIResponse[User], summary="创建新用户")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(is_admin)
):
    """创建新用户"""
    if userdao.get_user_by_username(db, username=user.username):
        raise BusinessException(msg="用户名已存在", code=400)

    if userdao.get_user_by_email(db, email=user.email):
        raise BusinessException(msg="邮箱已存在", code=400)

    new_user = userdao.create_user(db=db, user=user)
    return APIResponse(code=201, msg="用户创建成功", data=new_user)

@router.post("/update", response_model=APIResponse[User], summary="更新用户信息")
def update_user(
    params: UserUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(get_current_user)
):
    """更新用户信息（仅本人或管理员）"""
    db_user = userdao.get_user(db, user_id=params.user_id)
    if not db_user:
        raise BusinessException(msg="用户不存在", code=404)

    # 权限检查
    if db_user.id != current_user.id and current_user.role != "admin":
        raise BusinessException(msg="无权限修改", code=403)

    # 检查用户名冲突
    if params.username and params.username != db_user.username:
        if userdao.get_user_by_username(db, username=params.username):
            raise BusinessException(msg="用户名已存在", code=400)

    # 检查邮箱冲突
    if params.email and params.email != db_user.email:
        if userdao.get_user_by_email(db, email=params.email):
            raise BusinessException(msg="邮箱已存在", code=400)

    updated_user = userdao.update_user(db=db, db_user=db_user, user_update=params)
    return APIResponse(msg="用户更新成功", data=updated_user)

@router.post("/delete", response_model=APIResponse, summary="删除用户")
def delete_user(
    params: UserDelete,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(is_admin)
):
    """删除用户"""
    success = userdao.delete_user(db, user_id=params.user_id)
    if not success:
        raise BusinessException(msg="用户不存在", code=404)
    
    return APIResponse(msg="用户删除成功")
