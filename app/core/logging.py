import logging
from datetime import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

# 配置日志，明确指定UTF-8编码
logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s - %(levelname)s - %(message)s",
	handlers=[
		logging.FileHandler("access.log", encoding="utf-8"),  # 指定UTF-8编码
		logging.StreamHandler()  # 控制台输出
	]
)
logger = logging.getLogger("api_access")


class AccessLogMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
		# 记录请求开始时间
		start_time = datetime.now()

		# 获取基本信息
		client_ip = request.client.host if request.client else "unknown"
		method = request.method
		path = request.url.path
		query_params = dict(request.query_params)

		# 获取用户标识（可根据实际认证机制修改）
		user_identity = "anonymous"
		# 如果有认证系统，可以从request.state中获取用户信息
		# 例如: if hasattr(request.state, 'user'): user_identity = request.state.user.username

		# 获取请求体（对于非GET请求）
		request_body = {}
		if method != "GET":
			try:
				request_body = await request.json()
			except Exception:
				# 处理无法解析JSON的情况
				try:
					request_body = await request.body()
				except Exception as e:
					request_body = f"无法解析请求体: {str(e)}"

		# 处理请求
		response = await call_next(request)

		# 计算处理时间
		process_time = (datetime.now() - start_time).total_seconds()

		# 记录日志，确保支持中文等UTF-8字符
		log_message = (
			f"用户: {user_identity} | IP: {client_ip} | 方法: {method} | 路径: {path} | "
			f"查询参数: {query_params} | 请求体: {request_body} | "
			f"状态码: {response.status_code} | 处理时间: {process_time:.6f}秒"
		)
		logger.info(log_message)

		return response
