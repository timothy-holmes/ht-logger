import pickle

for_graph = {
    "bom_data": [
        {"d": 19208.19607638889,"t": 10.0},
        {"d": 19208.198391203703,"t": 11.0},
        {"d": 19208.206493055557, "t": 12.0},
        {"d": 19208.199548611112,"t": 13.0},
        {"d": 19208.20417824074,"t": 14.0}
    ],
    "shelly_h&t": [
        {"d": 19208.196087962962,"t": 9.0},
        {"d": 19208.198402777776,"t": 10.0},
        {"d": 19208.21650462963,"t": 11.0},
        {"d": 19208.199560185185,"t": 12.0},
        {"d": 19208.204189814816,"t": 13.0}
    ]
}

consume_url = '/consume?hum=70&temp=20.0&id=shellyht-test'

pickled_urls = {
    'http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json': './tests/ex_data/bom_req.pickle'
}

def pickled_request(url: str = None, filename: str = None):
    if not filename:
        filename = pickled_urls.get(url,None)
    if filename:
        with open(filename, 'rb') as rick:
            return pickle.load(rick)
    else:
        return None

if __name__ == '__main__':
    req = pickled_request(url='http://www.bom.gov.au/fwo/IDV60801/IDV60801.94865.json')
    data = req.json().get('observations',{}).get('data',{})
    print('\n'.join(ob['local_date_time_full'] for ob in data))
