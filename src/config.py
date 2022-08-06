from typing import Dict
from datetime import tzinfo
from zoneinfo import ZoneInfo
# don't put any src.* imports should be here 

class Config:
    sqlite_file_name: str = "/data/database.db"
    tz: tzinfo = ZoneInfo("Australia/Melbourne")
    sqlite_url: str = f"sqlite:///{sqlite_file_name}"
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
    bom_request_url: str = 'http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json' # Laverton station

config = Config()

