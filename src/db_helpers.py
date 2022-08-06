import os
from os.path import isfile, join
from datetime import datetime
import json

from sqlmodel import SQLModel, Session
from src.config import config as CONFIG
from src.models import Temperature

def create_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)

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
        url_params = data['query_string']
        details_list = url_params.split('&')
        detail_pairs_list = {p.split('=')[0]: p.split('=')[1]
                             for p in details_list}
        temperatures.append(
            Temperature(
                device_id = detail_pairs_list['id'],
                humidity = int(detail_pairs_list['hum']),
                temperature = float(detail_pairs_list['temp']),
                timestamp = datestamp
            )
        )
        # os.rename(file_path, file_path + '.bak')
    add_items_to_db(temperatures,engine)
   
def add_items_to_db(items,engine) -> bool:
    with Session(engine) as session:
        for item in items:
            session.add(item)
            print(item)
        session.commit()
    return True