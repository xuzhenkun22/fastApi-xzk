from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DayBase(BaseModel):
    year: str = "2025"
    month: str
    full_attendance_day: Optional[float] = None
    real_day: Optional[float] = None
    add_day: Optional[float] = None
    annual_leave_day: Optional[str] = None

class DayCreate(DayBase):
    pass

class DayUpdate(BaseModel):
    year: Optional[str] = None
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
