import pickle, requests
from datetime import datetime

from tests.config import test_config as CONFIG # same as src.cofig:config as CONFIG
print(__name__,CONFIG.sqlite_url)

def pickled_request(url: str):
    with open('./tests/ex_data/req_pickles.pickle','rb') as rick:
        request_d: dict = pickle.load(rick)
        if result := request_d['data'].get(url, None):
            result = pickle.loads(result)
    return result or requests.get(url=url,headers=CONFIG.bom_request_headers)

def repickle_urls():
    try:
        with open('./tests/ex_data/req_pickles.pickle','rb') as pickle_file:
            pickle_d: dict = pickle.load(pickle_file)
        if datetime.fromtimestamp(pickle_d['last_updated']) > datetime.timestamp(datetime.today()):
            return None
    except FileNotFoundError:
        pickle_d = {
            'data': {
                'http://www.bom.gov.au/fwo/IDT60901/IDT60901.94970.json': None,
                'http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json': None
            }
        }
    pickle_d['last_updated'] = int(datetime.timestamp(datetime.now(tz=CONFIG.tz))),
    for url in pickle_d['data'].keys():
        req = pickle.dumps(requests.get(url=url,headers=CONFIG.bom_request_headers))
        pickle_d['data'][url] = req
    with open('./tests/ex_data/req_pickles.pickle','wb') as pickle_file:
        pickle.dump(pickle_d,pickle_file)

def run_pickle_test():
    repickle_urls()
    req = pickled_request(url='http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json')
    data = req.json().get('observations',{}).get('data',{})
    print('\n'.join(ob['local_date_time_full'] for ob in data))
