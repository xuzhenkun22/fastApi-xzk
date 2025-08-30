import uvicorn
from config.config import DEFAULT_HOST, DEFAULT_PORT

if __name__ == "__main__":
    uvicorn.run(
        "config.main:app",
        host=DEFAULT_HOST,
        port=DEFAULT_PORT,
        reload=True
    )
