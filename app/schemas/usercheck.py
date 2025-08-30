from pydantic import BaseModel,EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """用户基础模型，包含公共字段"""
    username: str = Field(..., max_length=50, description="用户名")
    email: EmailStr
    role: Optional[str] = Field("user", pattern="^(user|admin)$", description="用户角色，只能是user或admin")

class UserCreate(UserBase):
    """创建用户时使用的模型，包含密码"""
    password: str = Field(..., min_length=6, description="用户密码，至少6个字符")

class UserUpdate(BaseModel):
    """更新用户时使用的模型，所有字段都是可选的"""
    username: Optional[str] = Field(None, max_length=50, description="新用户名")
    email: EmailStr
    password: Optional[str] = Field(None, min_length=6, description="新密码，至少6个字符")
    role: Optional[str] = Field(None, pattern="^(user|admin)$", description="新角色，只能是user或admin")

class UserInDBBase(UserBase):
    """数据库中用户的基础模型，包含ID"""
    id: int

    class Config:
        orm_mode = True

class User(UserInDBBase):
    """返回给客户端的用户模型"""
    pass

class UserInDB(UserInDBBase):
    """数据库中完整的用户模型，包含加密后的密码"""
    hashed_password: str
