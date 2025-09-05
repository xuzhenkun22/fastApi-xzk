from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """统一API响应模型"""
    success: bool = True
    data: Optional[T] = None
    total: Optional[int] = None

    errorCode:int =None
    errorMessage:str = ''

    showType:int = 0
    showMessage:str = ''

    class Config:
        orm_mode = True
