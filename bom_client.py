import requests

from datetime import date, datetime
from zoneinfo import ZoneInfo
tzinfo = ZoneInfo("Australia/Melbourne")

from models import engine, Temperature, add_items

from sqlmodel import Session, where, select

def convert_bom_timestamp(bom_timestamp: str):
    return datetime.timestamp(datetime(
                bom_timestamp[0:4], # year
                bom_timestamp[4:6], # month
                bom_timestamp[6:8], # day
                bom_timestamp[8:10], # hour
                bom_timestamp[10:12], # min
                bom_timestamp[12:14], # sec
                tzinfo = tzinfo 
    )) # TODO: there's probably a cleaner way of doing this using the dt format %Y%m%d%H%M%S%z?

def update_bom_data(last_bom_update: int):
    timestamp_now = datetime.timestamp(datetime.now())
    if timestamp_now - last_bom_update < 108000: 
        return last_bom_update
    else:
        bom_device_id = '087031_LAVERTON RAAF' # TODO: make config option
        with Session(engine) as session:
            query = select(Temperature)
            query = query.where(Temperature.device_id == bom_device_id)
            query = query.all()
            from_when = max(
                session.exec(query),
                key = lambda t: t.get('timestamp',0))
        new_temperatures = get_bom_data(from_when)
        add_items(new_temperatures)
        return timestamp_now

def get_bom_data(from_when):
    bom_station_obs_req = requests.get('http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json')
    if bom_station_obs_req.status_code == 200:
        obs = bom_station_obs_req.json().get('observations',{}).get('data',{})
    return [
        Temperature(
            device_id = '087031_LAVERTON RAAF',
            temperature = ob['air_temp'],
            humidity = ob['rel_hum'],
            timestamp = convert_bom_timestamp(ob['local_date_time_full']))
        for ob in obs
        if convert_bom_timestamp(ob['local_date_time_full']) > from_when]

