import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL")

# API配置
DEFAULT_HOST = os.getenv("DEFAULT_HOST")
DEFAULT_PORT = int(os.getenv("DEFAULT_PORT"))
API_PREFIX = os.getenv("API_PREFIX")

# 安全配置
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60*12  # 令牌有效期（分钟）
