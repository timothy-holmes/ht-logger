import pickle, requests
from datetime import datetime

from tests.config import test_config as CONFIG # interchanged for src.config:config

def pickled_request(url: str):
    with open(CONFIG.test_request_pickle_path,'rb') as rick:
        request_d: dict = pickle.load(rick)
        if result := request_d['data'].get(url, None):
            result = pickle.loads(result)
    return result or requests.get(url=url,headers=CONFIG.bom_request_headers)

def repickle_urls():
    try:
        with open(CONFIG.test_request_pickle_path,'rb') as pickle_file:
            pickle_d: dict = pickle.load(pickle_file)
        now = datetime.now(tz=CONFIG.tz)
        if pickle_d.get('last_updated',0) > datetime.timestamp(datetime(now.year,now.month,now.day)):
            return None
    except FileNotFoundError:
        pickle_d = {
            'data': {
                'http://www.bom.gov.au/fwo/IDT60901/IDT60901.94970.json': None,
                'http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json': None
            }
        }
    pickle_d['last_updated'] = int(datetime.timestamp(datetime.now(tz=CONFIG.tz)))
    for url in pickle_d['data'].keys():
        req = pickle.dumps(requests.get(url=url,headers=CONFIG.bom_request_headers))
        pickle_d['data'][url] = req
    with open(CONFIG.test_request_pickle_path,'wb') as pickle_file:
        pickle.dump(pickle_d,pickle_file)

def run_pickle_test():
    repickle_urls()
    req = pickled_request(url='http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json')
    data = req.json().get('observations',{}).get('data',{})
    print('\n'.join(ob['local_date_time_full'] for ob in data))

consume_url = '/consume?temp={}&hum={}&id={}'.format(30,69,'shellyht_f5dd')