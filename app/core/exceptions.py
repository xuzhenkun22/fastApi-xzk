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
            "errorCode": exc.code,
            "errorMessage": exc.msg,
            "data": None,
	        "success": False
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """FastAPI原生HTTP异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "errorCode": exc.status_code,
            "errorMessage": exc.detail,
            "data": None,
	        "success": False
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
            "errorCode": 400,
            "errorMessage": "参数验证失败："+str(errors),
	        "data"   : None,
	        "success": False
        }
    )

async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """数据库操作异常处理器"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "errorCode": 500,
            "errorMessage": "数据库操作失败",
            "data"   : None,
	        "success": False
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理器（未捕获的异常）"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "errorCode": 500,
            "errorMessage": "服务器内部错误",
            "data"   : None,
	        "success": False
        }
    )
