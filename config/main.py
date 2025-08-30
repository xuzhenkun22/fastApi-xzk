from fastapi import FastAPI
from app.api.router import api_router
from config.config import API_PREFIX
from config.database import Base, engine

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 初始化FastAPI应用
app = FastAPI(
    title="FastAPI MySQL Demo",
    description="A RESTful API demo using FastAPI and MySQL",
    version="1.0.0"
)

# 包含API路由
app.include_router(api_router, prefix=API_PREFIX)

@app.get("/", tags=["root"])
def read_root():
    """根路径，返回欢迎信息"""
    return {
        "message": "Welcome to FastAPI MySQL Demo API",
        "docs": "/docs",
        "redoc": "/redoc"
    }
