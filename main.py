""" Intraweb service for Shelly H&T devices """

import json
from datetime import datetime

from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from sqlmodel import create_engine, Session
import uvicorn

from config import config as CONFIG
from models import Temperature, add_items, create_db_and_tables
from bom_client import update_bom_data
from graphing import graph_n_days

app = FastAPI()
engine = create_engine(CONFIG['sqlite_url'])
session = Session(engine)

last_bom_update = 0

@app.get("/consume", response_class = PlainTextResponse)
async def consume_webhook(hum: int, temp: float, id: str) -> Temperature:
    timestamp = datetime.timestamp(datetime.now(tz=CONFIG['tz']))
    new_temperature = Temperature(
        timestamp = timestamp,
        humidity = hum,
        temperature = temp,
        device_id = id
    )
    await add_items([new_temperature],session)
    last_bom_update = update_bom_data(last_bom_update,session)
    return json.dumps({
        'message': 'Success',
        'timestamp': int(timestamp)
    },indent = 4)

@app.get("/status/{debug}", response_class = PlainTextResponse)
async def check_status(debug: int) -> dict:
    """Convience endpoint for confirming this app is operating. Returns sample string and datetime for now. """
    return json.dumps({
        'message': 'This message is evidence the app is running!',
        'datetime': bool(debug) or str(datetime.datetime.now()) # returns 1 if debug for testing 
    }, indent = 4)

@app.get("/last/{n_days}/days")
async def show_last_3_days(n_days: float):
    return Response(
        content = await graph_n_days(n=n_days), 
        media_type = 'image/png'
    )

if __name__ == '__main__':
    create_db_and_tables(engine)
    uvicorn.run(
        "main:app", 
        host = '0.0.0.0', 
        port=12345, 
        log_level="info"
    )