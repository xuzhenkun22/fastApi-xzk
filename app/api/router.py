from fastapi import APIRouter
from app.api.endpoints import attendance, roles, userapi, authapi

api_router = APIRouter()

# 包含路由
api_router.include_router(authapi.router, prefix="/auth", tags=["auth"])
api_router.include_router(userapi.router, prefix="/users", tags=["users"])
api_router.include_router(attendance.router, prefix="/attendance", tags=["attendance"])
api_router.include_router(roles.router, prefix="/security", tags=["security"])