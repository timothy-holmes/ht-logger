from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.main import session, engine
from src.models import Temperature, Device
from src.db_helpers import add_items_to_db

def test_db_filename():
    engine_repr = engine.__repr__().split('///')[-1]
    engine_filename = engine_repr[:-1]
    assert engine_filename == 'database.db.test'

def test_add_items():
    new_temperature = Temperature(
        device_id = 'shellyht-test',
        temperature = 20.0,
        hum = 70,
    )
    # add_items: returns True, gives 'not awaited warning'
    assert add_items_to_db([new_temperature],session)