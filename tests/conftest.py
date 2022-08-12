import sys, os
import pytest, requests
from sqlmodel import create_engine
from fastapi.testclient import TestClient
from tests.ex_data import pickled_request

# setup config
import src.config as config_temp # prod config
from tests.config import test_config # prod config with mods
module = config_temp
module.config = test_config # ignore incompatible type error
sys.modules['src.config'] = module # test config with further mods
from src.config import config as CONFIG
assert 'test' in CONFIG.sqlite_url

from src.main import app
from src.db_helpers import create_db_and_tables, add_items_to_db
from tests.ex_data import pickled_request, repickle_urls
from tests.ex_data.db_entries import generate_devices, generate_temperatures

# mocking response to cached requests
repickle_urls()

def mock_request_get(*args, **kwargs):
    url = kwargs.get('url', None) or args[0]
    if pickled_response := pickled_request(url):
        return pickled_response
    else:
        return requests.get(*args,**kwargs) 

module2 = requests 
# module = type(sys)['src.main']
module2.get = mock_request_get
sys.modules['requests'] = module2

@pytest.fixture()
def client():
    return TestClient(app)

# init engine
# using this approach because I want to use the engine
# in the pytest_sessionstart function below
db_engine = create_engine(CONFIG.sqlite_url)

@pytest.fixture()
def f_app():
    return app

@pytest.fixture()
def engine():
    return db_engine

def pytest_sessionstart(session):
    # delete existing test db
    if os.path.exists(CONFIG.sqlite_db_path):
        os.remove(CONFIG.sqlite_db_path)

    # create new test db with entries
    create_db_and_tables(db_engine)
    add_items_to_db(generate_temperatures(),db_engine)
    add_items_to_db(generate_devices(),db_engine)