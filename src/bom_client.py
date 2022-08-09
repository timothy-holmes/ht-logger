import requests
from datetime import datetime
from requests import HTTPError

from sqlmodel import select, Session

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.models import Temperature, Device
from src.main import engine
from src.db_helpers import add_items_to_db, get_last_updates

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
    timestamp_now = datetime.timestamp(datetime.now(tz = CONFIG.tz))
    new_temperatures = []
    for bom_station, last_update in get_last_updates(engine=engine, device_type='bom_station'):
        if last_update + CONFIG.bom_update_interval < timestamp_now: # more than 6 hours old
            new_temperatures.append(*_get_bom_data(device_id = bom_station, from_when = last_update))
    add_items_to_db(new_temperatures, engine)            

def _get_bom_data(device_id: str, from_when: float):
    with Session(engine) as session:
        url = session(select(Device).where(Device.device_id == device_id)).exec.all()[0].url
    obs_req = requests.get(
        url = url,
        headers = CONFIG.bom_request_headers
    )
    if obs_req.status_code == 200:
        obs = obs_req.json().get('observations',{}).get('data',{})
    else:
        pass
        print(HTTPError.__repr__())
    return [Temperature(
                device_id = device_id,
                temperature = ob['air_temp'],
                humidity = ob['rel_hum'],
                timestamp = convert_bom_timestamp(ob['local_date_time_full'])
            )
            for ob in obs
            if convert_bom_timestamp(ob['local_date_time_full']) > from_when]
