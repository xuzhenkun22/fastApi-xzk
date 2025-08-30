from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

class BusinessException(Exception):
    """自定义业务异常"""
    def __init__(self, msg: str, code: int = 400):
        self.msg = msg
        self.code = code
        super().__init__(self.msg)

async def custom_exception_handler(request: Request, exc: BusinessException):
    """自定义业务异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": exc.code,
            "msg": exc.msg,
            "data": None
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """FastAPI原生HTTP异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": exc.status_code,
            "msg": exc.detail,
            "data": None
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """请求参数验证异常处理器"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(map(str, error["loc"])),
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 400,
            "msg": "参数验证失败",
            "data": {"errors": errors}
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """数据库操作异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 500,
            "msg": "数据库操作失败",
            "data": None
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器（未捕获的异常）"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": 500,
            "msg": "服务器内部错误",
            "data": None
        }
    )
