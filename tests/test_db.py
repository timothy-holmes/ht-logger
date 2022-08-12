from src.config import config as CONFIG
from src.models import Temperature
from src.db_helpers import add_items_to_db

def test_db_filename(engine):
    engine_repr = engine.__repr__().split('///')
    engine_filename = engine_repr[-1][:-1]
    engine_filename_no_parameters = engine_filename.split('?')[0]
    assert 'test' in engine_filename_no_parameters

def test_add_items(engine):
    new_temperature = Temperature(
        device_id = 'shellyht-test',
        temperature = 20.0,
        hum = 70,
    )
    # add_items: returns True, gives 'not awaited warning'
    assert add_items_to_db([new_temperature],engine)