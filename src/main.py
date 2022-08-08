""" Intraweb service for Shelly H&T devices """

import json
from datetime import datetime

from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse
from sqlmodel import create_engine, Session, select

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)

app = FastAPI()
engine = create_engine(
    CONFIG.sqlite_url + '?check_same_thread=False'  # hacky :(
)

# circular imports
from src.models import Temperature
from src.bom_client import update_bom_data
from src.graphing import get_n_days, graph_n_days
from src.db_helpers import add_items_to_db, create_db_and_tables, add_old_data_to_db

@app.get("/consume", response_class = PlainTextResponse)
async def consume_webhook(hum: int, temp: float, id: str) -> str:
    timestamp = datetime.timestamp(datetime.now(tz=CONFIG.tz))
    new_temperature = Temperature(
        timestamp = timestamp,
        humidity = hum,
        temperature = temp,
        device_id = id
    )
    add_items_to_db([new_temperature],engine)
    last_bom_update = update_bom_data()
    return json.dumps({
        'message': 'Success',
        'timestamp': int(timestamp),
        'last_bom_update': last_bom_update
    },indent = 4)

@app.get("/status/{debug}", response_class = PlainTextResponse)
@app.get("/status", response_class = PlainTextResponse)
async def check_status(debug: int = 0) -> str:
    """Convience endpoint for confirming this app is operating. Returns sample string and datetime for now. """
    return json.dumps({
        'message': 'This message is evidence the app is running!',
        'datetime': bool(debug) or str(datetime.now(tz=CONFIG.tz)), # returns 1 if debug for testing 
        'last_bom_update': str(datetime.fromtimestamp(update_bom_data(), tz=CONFIG.tz))
    }, indent = 4)

@app.get("/last/{n_days}/days")
async def show_last_3_days(n_days: float) -> Response:
    dataset = await get_n_days(n_days,engine)
    return Response(
        content = (await graph_n_days(dataset)).read(), 
        media_type = 'image/png'
    )

# debugging only
@app.get("/db_dump", response_class = PlainTextResponse)
async def db_dump():
    with Session(engine) as session:
        return json.dumps(
            session.exec(select(Temperature)).all(),
            indent = 4
        )

def startup():
    print(engine)
    create_db_and_tables(engine)
    add_old_data_to_db(engine)