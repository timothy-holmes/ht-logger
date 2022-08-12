import requests
from datetime import datetime
from requests import HTTPError

from sqlmodel import select, Session

from src.config import config as CONFIG
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

def update_bom_data(check_age: bool = True):
    timestamp_now = datetime.timestamp(datetime.now(tz = CONFIG.tz))
    last_bom_updates = get_last_updates(engine=engine, device_type='bom_station')
    for bom_station, last_update in last_bom_updates.items():
        if check_age and (timestamp_now - last_update > CONFIG.bom_update_interval):
            add_items_to_db(_get_bom_data(device_id = bom_station, from_when = last_update), engine)
        elif not check_age:
            add_items_to_db(_get_bom_data(device_id = bom_station, from_when = last_update), engine)
    return [last_bom_updates,get_last_updates(engine=engine, device_type='bom_station')]

def _get_bom_data(device_id: str, from_when: float):
    with Session(engine) as session:
        url = session.exec(select(Device).where(Device.device_id == device_id)).all()[0].device_url
    obs_req = requests.get(
        url = url,
        headers = CONFIG.bom_request_headers
    )
    if obs_req.status_code == 200:
        obs = obs_req.json().get('observations',{}).get('data',{})
    else:
        pass
        print(HTTPError().__repr__())
    return [Temperature(
                device_id = device_id,
                temperature = ob['air_temp'],
                humidity = ob['rel_hum'],
                timestamp = convert_bom_timestamp(ob['local_date_time_full'])
            )
            for ob in obs
            if convert_bom_timestamp(ob['local_date_time_full']) > from_when]
