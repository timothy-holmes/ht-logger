import sys
import pytest, requests
from fastapi.testclient import TestClient
from tests.ex_data import pickled_request

# mocking import
# https://stackoverflow.com/questions/43162722/mocking-a-module-import-in-pytest
# this doesn't work because config (object) doesn't get created this way 
# module = type(sys)('src.config')
import src.config as config_temp # creates a sqlite file when importing
module = config_temp
module.config.sqlite_file_name += '.test'
module.config.sqlite_url += '.test'
sys.modules['src.config'] = module
from src.config import config as CONFIG
assert CONFIG.sqlite_url.endswith('.test')

from src.main import app, engine
from src.db_helpers import create_db_and_tables
from tests.ex_data import pickled_request

# mocking response to particular requests
def mock_request_get(*args, **kwargs):
    url = kwargs.get('url',None) or args[0]
    if pickled_response := pickled_request(url):
        return pickled_response
    else:
        return requests.get(*args,**kwargs) 

module2 = requests 
# module = type(sys)['src.main']
module2.get = mock_request_get
sys.modules['requests'] = module2

@pytest.fixture
def client():
    return TestClient(app)

def pytest_sessionstart(session):
    create_db_and_tables(engine)