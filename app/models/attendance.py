from sqlalchemy import Column, Integer, String, DECIMAL, DateTime
from datetime import datetime
from config.database import Base

class Day(Base):
    """考勤模型"""
    __tablename__ = "day"
    
    id = Column(Integer, primary_key=True, index=True, comment="考勤记录ID")
    month = Column(Integer, comment="月份")
    full_attendance_day = Column(DECIMAL(10, 1), comment="满勤天数（计薪）")
    real_day = Column(DECIMAL(10, 1), comment="实际出勤")
    add_day = Column(DECIMAL(10, 1), comment="贡献天数")
    annual_leave_day = Column(String(255), comment="年假天数")
    created_at = Column(DateTime, default=datetime.utcnow,  comment="创建时间")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")