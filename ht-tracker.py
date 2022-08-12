import uvicorn
from src.main import startup
from src.config import config as CONFIG

if __name__ == '__main__':
    startup()
    uvicorn.run(
        "src.main:app", 
        host = '0.0.0.0', 
        port=CONFIG.uvicorn_port, 
        log_level="info",
        reload=True
    )