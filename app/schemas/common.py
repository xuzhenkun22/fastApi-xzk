from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    """统一API响应模型"""
    code: int = 200
    msg: str = "success"
    data: Optional[T] = None

    class Config:
        orm_mode = True
