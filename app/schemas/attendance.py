from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DayBase(BaseModel):
    month: str
    full_attendance_day: Optional[float] = None
    real_day: Optional[float] = None
    add_day: Optional[float] = None
    annual_leave_day: Optional[str] = None

class DayQuery(BaseModel):
    """用户列表查询模型"""
    current: int = Field(0, ge=0, description="跳过的记录数")
    pageSize: int = Field(100, ge=1, le=500, description="每页记录数（1-500）")
    month: Optional[str] = None

class DayCreate(DayBase):
    pass

class DayUpdate(BaseModel):
    month: Optional[str] = None
    full_attendance_day: Optional[float] = None
    real_day: Optional[float] = None
    add_day: Optional[float] = None
    annual_leave_day: Optional[str] = None

class DayInDBBase(DayBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class Day(DayInDBBase):
    pass
