import requests, pickle

class CONFIG:
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

def update_bom_request_pickle():
    req = requests.get(CONFIG.bom_request_url,headers=CONFIG.bom_request_headers)
    with open('tests/ex_data/bom_req.pickle','wb') as rick:
        pickle.dump(req,rick)

if __name__ == '__main__':
    update_bom_request_pickle()