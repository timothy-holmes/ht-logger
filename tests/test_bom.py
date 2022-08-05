from datetime import datetime

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.bom_client import convert_bom_timestamp, get_bom_data, get_last_bom_update, update_bom_data

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

def test_get_bom_data_all():
    now = datetime.timestamp(datetime.now(CONFIG.tz))
    bom_data = get_bom_data(0)
    for result in bom_data:
        assert result.device_id == '087031_LAVERTON RAAF'
        assert result.temperature > -20 # realistic bounds
        assert result.temperature < 60
        assert result.humidity > 0 # physcial bounds
        assert result.humidity < 100
        assert result.timestamp + 4 * 86400 + 3 * 3600> now # recent - 3 days + 3 hours

def test_get_bom_data_none():
    now = datetime.timestamp(datetime.now(CONFIG.tz)) + 3600
    bom_data = get_bom_data(now)
    assert len(bom_data) == 0

def test_get_bom_data_some():
    now = datetime.timestamp(datetime.now(CONFIG.tz)) - 12*3600
    bom_data = get_bom_data(now)
    assert len(bom_data) < 24
    assert len(bom_data) > 0

def test_get_last_bom_update():
    device_id = '087031_LAVERTON RAAF'
    update = get_last_bom_update(device_id)
    assert (update == 0) or (update > 1659000000)

def test_update_bom_data():
    timestamp_now = datetime.timestamp(datetime.now(CONFIG.tz))
    assert timestamp_now - update_bom_data() < 6 * 3600


