from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any

from app.core.dependencies import check_permission
from config.database import get_db
from app.schemas.role import Role, RoleCreate, RoleUpdate, Permission, PermissionCreate
from app.crud.roledao import (
    get_role, get_roles, get_role_by_name, create_role, update_role, delete_role,
    get_permission, get_permissions, get_permission_by_code, create_permission,
    add_permission_to_role, remove_permission_from_role
)
from app.models.user import User as DBUser

router = APIRouter()

# 角色管理
@router.get("/roles", response_model=List[Role])
def read_roles(
    current: int = 0,
    pageSize: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """获取角色列表（需要角色管理权限）"""
    roles = get_roles(db, current=current, pageSize=pageSize)
    return roles

@router.post("/roles", response_model=Role, status_code=status.HTTP_201_CREATED)
def create_new_role(
    role: RoleCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """创建新角色（需要角色管理权限）"""
    db_role = get_role_by_name(db, name=role.name)
    if db_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色名称已存在"
        )
    return create_role(db=db, role=role)

@router.get("/roles/{role_id}", response_model=Role)
def read_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """获取指定角色信息（需要角色管理权限）"""
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    return db_role

@router.put("/roles/{role_id}", response_model=Role)
def update_existing_role(
    role_id: int,
    role: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """更新角色信息（需要角色管理权限）"""
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="角色不存在")
    
    # 检查角色名是否已被占用
    if role.name:
        existing_role = get_role_by_name(db, name=role.name)
        if existing_role and existing_role.id != role_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="角色名称已存在"
            )
    
    return update_role(db=db, db_role=db_role, role_update=role)

@router.delete("/roles/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_role(
    role_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """删除角色（需要角色管理权限）"""
    success = delete_role(db, role_id=role_id)
    if not success:
        raise HTTPException(status_code=404, detail="角色不存在")
    return None

# 权限管理
@router.get("/permissions", response_model=List[Permission])
def read_permissions(
    current: int = 0,
    pageSize: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """获取权限列表（需要角色管理权限）"""
    permissions = get_permissions(db, current=current, pageSize=pageSize)
    return permissions

@router.post("/permissions", response_model=Permission, status_code=status.HTTP_201_CREATED)
def create_new_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """创建新权限（需要角色管理权限）"""
    db_perm = get_permission_by_code(db, code=permission.code)
    if db_perm:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="权限标识已存在"
        )
    return create_permission(db=db, permission=permission)

# 角色权限关联
@router.post("/roles/{role_id}/permissions/{permission_id}", response_model=Dict[str, Any])
def assign_permission_to_role(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """为角色分配权限（需要角色管理权限）"""
    success = add_permission_to_role(db, role_id=role_id, permission_id=permission_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色或权限不存在，或权限已分配"
        )
    return {"message": "权限分配成功", "role_id": role_id, "permission_id": permission_id}

@router.delete("/roles/{role_id}/permissions/{permission_id}", response_model=Dict[str, Any])
def remove_permission_from_role_endpoint(
    role_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("role:manage"))
):
    """从角色移除权限（需要角色管理权限）"""
    success = remove_permission_from_role(db, role_id=role_id, permission_id=permission_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="角色或权限不存在，或权限未分配"
        )
    return {"message": "权限移除成功", "role_id": role_id, "permission_id": permission_id}
