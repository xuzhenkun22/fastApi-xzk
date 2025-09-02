from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import check_permission
from config.database import get_db
from app.schemas.attendance import Day, DayCreate, DayUpdate
from app.crud.attendancedao import (
    get_day, get_days, get_days_by_month,
    create_day, update_day, delete_day
)
from app.models.user import User as DBUser

router = APIRouter()

@router.get("/", response_model=List[Day])
def read_attendance_records(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("attendance:view"))
):
    """获取考勤记录列表（需要查看考勤权限）"""
    days = get_days(db, skip=skip, limit=limit)
    return days

@router.get("/month/{year}/{month}", response_model=List[Day])
def read_attendance_by_month(
    year: str,
    month: str,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("attendance:view"))
):
    """按月份获取考勤记录（需要查看考勤权限）"""
    days = get_days_by_month(db, year=year, month=month)
    return days

@router.post("/", response_model=Day, status_code=status.HTTP_201_CREATED)
def create_attendance_record(
    day: DayCreate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("attendance:manage"))
):
    """创建新考勤记录（需要管理考勤权限）"""
    return create_day(db=db, day=day)

@router.get("/{day_id}", response_model=Day)
def read_attendance_record(
    day_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("attendance:view"))
):
    """获取指定考勤记录（需要查看考勤权限）"""
    db_day = get_day(db, day_id=day_id)
    if db_day is None:
        raise HTTPException(status_code=404, detail="考勤记录不存在")
    return db_day

@router.put("/{day_id}", response_model=Day)
def update_attendance_record(
    day_id: int,
    day: DayUpdate,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("attendance:manage"))
):
    """更新考勤记录（需要管理考勤权限）"""
    db_day = get_day(db, day_id=day_id)
    if db_day is None:
        raise HTTPException(status_code=404, detail="考勤记录不存在")
    return update_day(db=db, db_day=db_day, day_update=day)

@router.delete("/{day_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance_record(
    day_id: int,
    db: Session = Depends(get_db),
    current_user: DBUser = Depends(check_permission("attendance:manage"))
):
    """删除考勤记录（需要管理考勤权限）"""
    success = delete_day(db, day_id=day_id)
    if not success:
        raise HTTPException(status_code=404, detail="考勤记录不存在")
    return None
