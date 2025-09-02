from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from config.database import Base

# 角色-权限关联表
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("role_id", Integer, ForeignKey("roles.id"), comment="角色ID"),
    Column("permission_id", Integer, ForeignKey("permissions.id"), comment="权限ID")
)

class Role(Base):
    """角色模型"""
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True, comment="角色ID")
    name = Column(String(50), unique=True, index=True, nullable=False, comment="角色名称")
    description = Column(String(255), comment="角色描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")
    
    # 关联权限
    permissions = relationship("Permission", secondary=role_permissions, back_populates="roles")

class Permission(Base):
    """权限模型"""
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True, comment="权限ID")
    name = Column(String(100), nullable=False, comment="权限名称")
    code = Column(String(100), unique=True, index=True, nullable=False, comment="权限标识")
    description = Column(String(255), comment="权限描述")
    created_at = Column(DateTime, default=datetime.utcnow, comment="创建时间")
    
    # 关联角色
    roles = relationship("Role", secondary=role_permissions, back_populates="permissions")
