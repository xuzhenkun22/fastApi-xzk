from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    """用户基本信息模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    role: str = Field("user", pattern="^(admin|user)$", description="角色：admin/user")

class UserCreate(UserBase):
    """创建用户请求模型"""
    password: str = Field(..., min_length=6, description="密码（至少6位）")

class UserUpdate(BaseModel):
    """更新用户请求模型"""
    user_id: int = Field(..., description="用户ID")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    password: Optional[str] = Field(None, min_length=6, description="密码（至少6位）")
    role: Optional[str] = Field(None, pattern="^(admin|user)$", description="角色：admin/user")

class UserQuery(BaseModel):
    """用户列表查询模型"""
    current: int = Field(0, ge=0, description="跳过的记录数")
    pageSize: int = Field(100, ge=1, le=500, description="每页记录数（1-500）")

class UserGet(BaseModel):
    """获取单个用户请求模型"""
    user_id: int = Field(..., gt=0, description="用户ID")

class UserDelete(BaseModel):
    """删除用户请求模型"""
    user_id: int = Field(..., gt=0, description="用户ID")

class LoginRequest(BaseModel):
    """登录请求模型"""
    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

class User(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    created_at: Optional[str]

    class Config:
        orm_mode = True
