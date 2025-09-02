from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.exceptions import BusinessException, custom_exception_handler
from app.core.exceptions import general_exception_handler, http_exception_handler, sqlalchemy_exception_handler, \
	validation_exception_handler
from app.core.logging import AccessLogMiddleware
from config.config import API_PREFIX
# 创建数据库表
from config.database import Base, engine

Base.metadata.create_all(bind=engine)

# 初始化FastAPI应用
app = FastAPI(
    title="FastAPI Project",
    description="A FastAPI project with unified response format and authentication",
    version="1.0.0"
)

# 注册异常处理器
app.add_exception_handler(BusinessException, custom_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
app.add_middleware(AccessLogMiddleware)
# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应指定具体的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# 注册路由
app.include_router(api_router, prefix=API_PREFIX)

# 根路径
@app.get("/")
def read_root():
    return {"message": "欢迎使用fastApi项目模板!"}
