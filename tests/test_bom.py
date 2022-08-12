from datetime import datetime

from sqlmodel import select, Session

from src.config import config as CONFIG
from src.bom_client import convert_bom_timestamp, _get_bom_data, update_bom_data
from src.models import Temperature, Device


def test_convert_bom_timestamp():
    now: datetime = datetime.now(CONFIG.tz)
    test_time = datetime(
        now.year, now.month, now.day,
        now.hour, now.minute, now.second, 
        tzinfo = CONFIG.tz
    )
    test_time_timestamp = datetime.timestamp(test_time)
    test_time_str = test_time.strftime('%Y%m%d%H%M%S')
    assert convert_bom_timestamp(test_time_str) == test_time_timestamp

def test_get_bom_data_all(engine):
    with Session(engine) as session:
        bom_device = session.exec(select(Device).where(Device.device_type == 'BOM_json')).first()
    bom_data = _get_bom_data(bom_device.device_id,0)
    assert len(bom_data) > 0
    for result in bom_data:
        assert result.temperature > -20 # realistic bounds
        assert result.temperature < 45
        assert result.humidity > 0 # physcial bounds
        assert result.humidity < 100

def test_update_bom_data(engine):
    with Session(engine) as session:
        if not len(session.exec(select(Temperature)).all()):
            update_bom_data(check_age=False)
        assert len(session.exec(select(Temperature)).all()) > 0