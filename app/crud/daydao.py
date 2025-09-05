from sqlalchemy.orm import Session
from typing import List, Optional

from app.models.attendance import Day
from app.schemas.day import DayCreate


def get_user(db: Session, id: int) -> Optional[Day]:
    return db.query(Day).filter(Day.id == id).first()

def get_users(db: Session, current: int = 0, pageSize: int = 100) -> List[Day]:
    """获取用户列表（分页）"""
    return db.query(Day).offset(current).limit(pageSize).all()

def create_user(db: Session, user: DayCreate) -> Day:
    """创建新用户"""
    hashed_password = get_password_hash(user.password)
    db_user = Day(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: Day, user_update: DayUpdate) -> Day:
    """更新用户信息"""
    update_data = user_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: int) -> bool:
    """删除用户"""
    user = db.query(Day).filter(Day.id == id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False

def authenticate_user(db: Session, username: str, password: str) -> Optional[Day]:
    """验证用户身份"""
    user = get_user_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
