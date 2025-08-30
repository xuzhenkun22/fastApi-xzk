import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:xzk0422@127.0.0.1:3306/xzk")

# API配置
DEFAULT_HOST = os.getenv("DEFAULT_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("DEFAULT_PORT", 4222))
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")

# 安全配置
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-keep-it-safe")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 令牌有效期（分钟）
