import uvicorn
from src.main import startup

if __name__ == '__main__':
    startup()
    uvicorn.run(
        "src.main:app", 
        host = '0.0.0.0', 
        port=12345, 
        log_level="info"
    )