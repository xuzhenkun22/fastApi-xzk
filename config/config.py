import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 数据库配置
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:xzk0422@127.0.0.1:3306/xzk")

# API默认配置
DEFAULT_HOST = os.getenv("DEFAULT_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.getenv("DEFAULT_PORT", 4222))
API_PREFIX = os.getenv("API_PREFIX", "/api/v1")
