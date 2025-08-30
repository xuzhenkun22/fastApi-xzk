from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from config.config import SECRET_KEY, ALGORITHM
from config.database import get_db
from app.crud import userdao
from app.models.userdb import User
from app.core.exceptions import BusinessException

# OAuth2令牌提取器
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """获取当前登录用户"""
    print('Token:', token)  # 调试输出
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise BusinessException(msg="无法验证凭据", code=401)
    except JWTError:
        raise BusinessException(msg="无法验证凭据", code=401)
    print('user_id:', user_id)  # 调试输出
    user = userdao.get_user(db, user_id=int(user_id))

    if user is None:
        raise BusinessException(msg="用户不存在", code=401)
    return user

def is_admin(current_user: User = Depends(get_current_user)) -> User:
    """验证是否为管理员"""
    print('current_user:', current_user)  # 调试输出
    if current_user.role != "admin":
        raise BusinessException(msg="没有权限执行此操作", code=403)
    return current_user
