from sqlalchemy.orm import Session
from sqlalchemy import desc, tuple_
from typing import List, Optional
from app.models.attendance import Day
from app.schemas.attendance import DayCreate, DayUpdate


def get_days(db: Session, current: int = 0, pageSize: int = 100,month:str ='') -> dict[str, object]:
	"""获取考勤记录列表（分页）"""
	query = db.query(Day).filter(Day.month <= month).order_by(desc(Day.month)).limit(12)
	total = query.count()
	data = query.offset((current - 1) * pageSize).limit(pageSize).all()
	return {
		"total": total,
		"data": data
	}

def create_day(db: Session, day: DayCreate) -> Day:
	"""创建新考勤记录"""
	db_day = Day(
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
