from math import inf
from typing import Optional
from zoneinfo import ZoneInfo
from datetime import datetime

from sqlmodel import Field, SQLModel

tzinfo = ZoneInfo("Australia/Melbourne")

class Temperature(SQLModel, table=True):
    id: int = Field(default=None, primary_key = True)
    device_id: str
    temperature: float = 0
    humidity: Optional[int] = None
    timestamp: float = datetime.timestamp(datetime.now(tz=tzinfo))

class Device(SQLModel, table=True):
    id: int = Field(default=None, primary_key = True)
    device_id: str
    friendly_name: str
    start_timestamp: Optional[float] = 0
    end_timestamp: Optional[float] = inf

def create_db_and_tables():
    SQLModel.metadata.create_all()

async def add_items(items,session):
    for item in items:
        session.add(item)
    session.commit()
