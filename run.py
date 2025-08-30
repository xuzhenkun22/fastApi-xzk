import uvicorn
import argparse

from config.config import DEFAULT_HOST, DEFAULT_PORT


def main():
    """启动FastAPI应用"""
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="Run the FastAPI application.")
    parser.add_argument(
        "--host", 
        type=str, 
        default=DEFAULT_HOST, 
        help=f"Host to run the server on (default: {DEFAULT_HOST})"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=DEFAULT_PORT, 
        help=f"Port to run the server on (default: {DEFAULT_PORT})"
    )
    parser.add_argument(
        "--reload", 
        action="store_true", 
        help="Enable auto-reload for development"
    )
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 启动Uvicorn服务器
    uvicorn.run(
        "config.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload
    )

if __name__ == "__main__":
    main()
