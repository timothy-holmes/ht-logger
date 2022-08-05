from os import listdir
from os.path import isfile, join

from sqlmodel import SQLModel

def create_db_and_tables(engine) -> None:
    SQLModel.metadata.create_all(engine)

# def add_old_data_to_db():
#     old_dta_path = './data/old_data'
#     req_files = [f for f in listdir(mypath) 
#                  if isfile(join(mypath, f))]
#     for file in onlyfiles:

async def add_items_to_db(items,session) -> bool:
    for item in items:
        session.add(item)
    session.commit()
    return True