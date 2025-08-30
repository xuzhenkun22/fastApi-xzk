from sqlalchemy import Column, Integer, String

from config.database import Base


class User(Base):
    """数据库用户模型，与users表对应"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="用户主键ID")
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名（唯一）")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="用户邮箱（唯一）")
    hashed_password = Column(String(100), nullable=False, comment="加密后的密码")
    role = Column(String(20), default="user", nullable=False, comment="用户角色（user：普通用户，admin：管理员）")
