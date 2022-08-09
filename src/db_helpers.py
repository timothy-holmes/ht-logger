import os, json
from os.path import isfile, join
from datetime import datetime
from typing import Optional

from sqlmodel import Session, select
from src.config import config as CONFIG
from src.models import Temperature, Device

# def db_engine():
    # yield engine

# def migrate():

def add_items_to_db(items,engine) -> bool:
    with Session(engine) as session:
        for item in items:
            session.add(item)
            print(item)
        session.commit()
    return True
    
def add_old_data_to_db(engine):
    temperatures = []
    old_data_path = '/data/old_data'
    req_files = [f for f in os.listdir(old_data_path) 
                 if isfile(join(old_data_path, f)) and
                    f.endswith('.json')]
    for file in req_files:
        file_date = file.split('-')[-1].split('.')[0]
        datestamp = datetime.timestamp(datetime(
                int(file_date[0:4]), # year
                int(file_date[4:6]), # month
                int(file_date[6:8]), # day
                int(file_date[8:10]), # hour
                int(file_date[10:12]), # min
                int(file_date[12:14]), # sec
                tzinfo = CONFIG.tz
        ))
        file_path = join(old_data_path, file)
        with open(file_path,'r') as json_file:
            data = json.load(json_file)
        url_params = data.get('query_string','')
        if url_params:
            details_list = url_params.split('&')
            detail_pairs_list = {p.split('=')[0]: p.split('=')[1]
                                for p in details_list}
            if all(x in detail_pairs_list.keys() for x in ['hum','id','temp']):
                temperatures.append(
                    Temperature(
                        device_id = detail_pairs_list['id'],
                        humidity = int(detail_pairs_list['hum']),
                        temperature = float(detail_pairs_list['temp']),
                        timestamp = datestamp
                    )
                )
        os.rename(file_path, file_path + '.bak')
    add_items_to_db(temperatures,engine)

def get_last_update(device_id: str, engine) -> float:
    query = select(Temperature)
    query = query.where(Temperature.device_id == device_id)
    with Session(engine) as session:
        results: list[Temperature] = session.exec(query).all()
    return max([t.timestamp for t in results] + [0])

def get_last_updates(engine, device_type: Optional[str]) -> dict[str, float]:
    query = select(Device) # limit to device_id column only
    if device_type:
        query = query.where(Device.device_type == device_type)
    with Session(engine) as session:
        results: list[Device] = session.exec(query).all()
    return {d.device_id: get_last_update(d.device_id) for d in results}