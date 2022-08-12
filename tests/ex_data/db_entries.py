from datetime import datetime, timedelta

from src.models import Temperature, Device
from tests.config import test_config as CONFIG

devices = [
    {
        'device_id': 'shellyht_f5dd', 
        'friendly_name': 'Raelia', 
        'device_type': 'ShellyHT', 
    },
    {
        'device_id': 'shellyht_e651', 
        'friendly_name': 'Outside', 
        'device_type': 'ShellyHT', 
    },
    {
        'device_id': 'BOM_94970', 
        'friendly_name': 'BOM Hobart Station', 
        'device_type': 'BOM_json', 
        'device_url': 'http://www.bom.gov.au/fwo/IDT60901/IDT60901.94970.json'
    },
    {
        'device_id': 'BOM_94865', 
        'friendly_name': 'BOM Laverton Station', 
        'device_type': 'BOM_json', 
        'device_url': 'http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json'
    },
]

temperature_func = [
    lambda x: (x % 3) * 4, # 0,4,8,12
    lambda x: (15 - x % 10) # 6 to 15
]

timestamp = range(
        int(datetime.timestamp(datetime.now(tz=CONFIG.tz) - timedelta(hours=24))),
        int(datetime.timestamp(datetime.now(tz=CONFIG.tz) - timedelta(minutes=96))),
        48 * 60
    )

def generate_temperatures():
    temperatures = []
    shelly_devices = [d['device_id'] for d in devices if d['device_type'] == 'ShellyHT']
    for x,shelly_device in enumerate(shelly_devices):
        for y,t in enumerate(timestamp):
            temperatures.append(
                Temperature(
                    device_id = shelly_device,
                    temperature = temperature_func[x](y),
                    timestamp = t,
                    humidity = 69,
                )
            )
    return temperatures

def generate_devices():
    return [Device(**device) for device in devices]