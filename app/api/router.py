from fastapi import APIRouter
from app.api.endpoints import userapi

# 创建主API路由
api_router = APIRouter()

# 包含各个端点的路由
api_router.include_router(userapi.router, prefix="/users", tags=["users"])  # 添加用户路由
