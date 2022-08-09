from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)

class Temperature(SQLModel, table=True):
    id: int = Field(default=None, primary_key = True)
    device_id: str
    temperature: float = 0
    humidity: Optional[int] = None
    timestamp: float = datetime.timestamp(datetime.now(tz=CONFIG.tz))

class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key = True)
    device_id: str
    friendly_name: str
    device_type: str # 'shelly' or 'bom_station'
    device_url: Optional[str]