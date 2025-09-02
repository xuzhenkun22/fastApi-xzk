from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.role_permission import Role, Permission
from app.schemas.role import RoleCreate, RoleUpdate, PermissionCreate

def get_role(db: Session, role_id: int) -> Optional[Role]:
    return db.query(Role).filter(Role.id == role_id).first()

def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    return db.query(Role).filter(Role.name == name).first()

def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    return db.query(Role).offset(skip).limit(limit).all()

def create_role(db: Session, role: RoleCreate) -> Role:
    db_role = Role(name=role.name, description=role.description)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def update_role(db: Session, db_role: Role, role_update: RoleUpdate) -> Role:
    update_data = role_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_role, key, value)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def delete_role(db: Session, role_id: int) -> bool:
    role = db.query(Role).filter(Role.id == role_id).first()
    if role:
        db.delete(role)
        db.commit()
        return True
    return False

# 权限相关操作
def get_permission(db: Session, permission_id: int) -> Optional[Permission]:
    return db.query(Permission).filter(Permission.id == permission_id).first()

def get_permission_by_code(db: Session, code: str) -> Optional[Permission]:
    return db.query(Permission).filter(Permission.code == code).first()

def get_permissions(db: Session, skip: int = 0, limit: int = 100) -> List[Permission]:
    return db.query(Permission).offset(skip).limit(limit).all()

def create_permission(db: Session, permission: PermissionCreate) -> Permission:
    db_perm = Permission(
        name=permission.name, 
        code=permission.code, 
        description=permission.description
    )
    db.add(db_perm)
    db.commit()
    db.refresh(db_perm)
    return db_perm

# 角色权限关联操作
def add_permission_to_role(db: Session, role_id: int, permission_id: int) -> bool:
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission and permission not in role.permissions:
        role.permissions.append(permission)
        db.commit()
        return True
    return False

def remove_permission_from_role(db: Session, role_id: int, permission_id: int) -> bool:
    role = get_role(db, role_id)
    permission = get_permission(db, permission_id)
    if role and permission and permission in role.permissions:
        role.permissions.remove(permission)
        db.commit()
        return True
    return False
