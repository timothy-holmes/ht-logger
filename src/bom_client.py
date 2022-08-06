import requests
from datetime import datetime
from requests import HTTPError

from sqlmodel import select, Session

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.models import Temperature
from src.main import engine
from src.db_helpers import add_items_to_db

def convert_bom_timestamp(bom_timestamp: str):
    return datetime.timestamp(datetime(
                int(bom_timestamp[0:4]), # year
                int(bom_timestamp[4:6]), # month
                int(bom_timestamp[6:8]), # day
                int(bom_timestamp[8:10]), # hour
                int(bom_timestamp[10:12]), # min
                int(bom_timestamp[12:14]), # sec
                tzinfo = CONFIG.tz
    )) # TODO: there's probably a cleaner way of doing this using dt format %Y%m%d%H%M%S%z?

def update_bom_data():
    timestamp_now = datetime.timestamp(datetime.now(CONFIG.tz))
    bom_device_id = '087031_LAVERTON RAAF' # TODO: make multiple om sites config option
    last_bom_update = get_last_bom_update(bom_device_id)
    if last_bom_update + 108000 < timestamp_now: # more than 6 hours old
        new_temperatures = _get_bom_data(from_when = last_bom_update)
        add_items_to_db(new_temperatures, engine)
        return timestamp_now
    else:
        return last_bom_update

def get_last_bom_update(bom_device_id):
    # TODO: generalise this function (not just bom devices)
    #       more to db_helpers.py
    #       add results to status check endpoint
    query = select(Temperature)
    query = query.where(Temperature.device_id == bom_device_id)
    with Session(engine) as session:
        results: list[Temperature] = session.exec(query).all()
    last_bom_update = max([t.timestamp for t in results] + [0])
    return last_bom_update

def _get_bom_data(from_when: float):
    bom_station_obs_req = requests.get(
        url = CONFIG.bom_request_url,
        headers = CONFIG.bom_request_headers
    )
    if bom_station_obs_req.status_code == 200:
        obs = bom_station_obs_req.json().get('observations',{}).get('data',{})
    else:
        raise HTTPError
    return [
        Temperature(
            device_id = '087031_LAVERTON RAAF',
            temperature = ob['air_temp'],
            humidity = ob['rel_hum'],
            timestamp = convert_bom_timestamp(ob['local_date_time_full']))
        for ob in obs
        if convert_bom_timestamp(ob['local_date_time_full']) > from_when]
