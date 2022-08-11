from typing import Dict
import os.path
from datetime import tzinfo
from zoneinfo import ZoneInfo
# don't put any src.* imports should be here 

class ConfigData:
    bom_request_headers: dict[str, str] = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Host': 'www.bom.gov.au',
        'Pragma': 'no-cache',
        'Referer': 'http://www.bom.gov.au/products/IDV60801/IDV60801.94865.shtml',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    bom_update_interval: int = 10800 # 3 hours between updates
    data_volume_path: str = os.env.get('HT_DATA_VOLUME_PATH') or './data'
    sqlite_db_filename: str = "database.db"
    tz: tzinfo = ZoneInfo("Australia/Melbourne")

class Config(ConfigData):
    sqlite_db_path: str = os.path.abspath(os.path.join(data_volume_path,sqlite_db_filename))
    sqlite_url: str = f"sqlite:///{sqlite_db_path}"

config = Config()
