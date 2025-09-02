from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.attendance import Day
from app.schemas.attendance import DayCreate, DayUpdate

def get_day(db: Session, day_id: int) -> Optional[Day]:
    """根据ID获取考勤记录"""
    return db.query(Day).filter(Day.id == day_id).first()

def get_days_by_month(db: Session, year: str, month: str) -> List[Day]:
    """根据年月获取考勤记录"""
    return db.query(Day).filter(Day.year == year, Day.month == month).all()

def get_days(db: Session, skip: int = 0, limit: int = 100) -> List[Day]:
    """获取考勤记录列表（分页）"""
    return db.query(Day).offset(skip).limit(limit).all()

def create_day(db: Session, day: DayCreate) -> Day:
    """创建新考勤记录"""
    db_day = Day(
        year=day.year,
        month=day.month,
        full_attendance_day=day.full_attendance_day,
        real_day=day.real_day,
        add_day=day.add_day,
        annual_leave_day=day.annual_leave_day
    )
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return db_day

def update_day(db: Session, db_day: Day, day_update: DayUpdate) -> Day:
    """更新考勤记录"""
    update_data = day_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_day, key, value)
    db.add(db_day)
    db.commit()
    db.refresh(db_day)
    return db_day

def delete_day(db: Session, day_id: int) -> bool:
    """删除考勤记录"""
    day = db.query(Day).filter(Day.id == day_id).first()
    if day:
        db.delete(day)
        db.commit()
        return True
    return False
