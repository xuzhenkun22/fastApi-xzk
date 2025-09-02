from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

class User(Base):
    """用户模型"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, comment="用户主键ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名（唯一）")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="用户邮箱（唯一）")
    hashed_password = Column(String(100), nullable=False, comment="加密后的密码")
    role = Column(String(20), default="user", nullable=False, comment="用户角色（user：普通用户，admin：管理员）")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    avatar = Column(String(255),  comment="头像")
    signature = Column(String(255),  comment="个性签名")
    title = Column(String(255),  comment="抬头")
    phone = Column(String(255),  comment="手机号")
    group = Column(String(255),  comment="部门")



