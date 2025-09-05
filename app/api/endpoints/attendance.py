import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.exceptions import BusinessException
from app.crud import attendancedao
from app.schemas.common import APIResponse
from config.database import get_db
from app.schemas.attendance import Day, DayCreate, DayInDBBase, DayQuery, DayUpdate


router = APIRouter()


@router.post("/list", response_model=APIResponse[List[Day]], summary="获取出勤记录")
def read_users(
	params: DayQuery,
	db: Session = Depends(get_db),
):
	"""获取出勤记录（分页）"""
	if params.pageSize > 500:
		raise BusinessException(msg="每页最大记录数不能超过500", code=400)
	if params.month is None or params.month == '':
		params.month =datetime.date.today().strftime("%Y-%m")

	ret = attendancedao.get_days(db, current=params.current, pageSize=params.pageSize,month = params.month)
	return APIResponse(data=ret.get("data"), total=ret.get("total"))

@router.post("/add", response_model=APIResponse[List[Day]], summary="新增出勤记录")
def read_users(
	params: DayCreate,
	db: Session = Depends(get_db),
):
	"""新增出勤记录"""
	ret = attendancedao.create_day(db, day=params)
	return APIResponse(data = [ret])

@router.post("/del", response_model=APIResponse[List[Day]], summary="删除出勤记录")
def read_users(
	params: DayInDBBase,
	db: Session = Depends(get_db),
):
	"""新增出勤记录"""
	attendancedao.delete_day(db, day_id=params.id)
	return APIResponse(data = [])