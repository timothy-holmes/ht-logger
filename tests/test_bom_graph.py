from datetime import datetime

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.bom_client import get_bom_data
from src.graphing import graph_n_days

def test_bom_graph():
    bom_data = get_bom_data(0)
    points = list(sorted(bom_data, key=lambda p: p.timestamp))
    devices = set(p.device_id for p in points)
    dataset = {
        d: [{
                'd': p.timestamp / 86400, # convert from seconds to days
                't': p.temperature
            }
            for p in points if p.device_id == d]
            for d in devices}
    graph = graph_n_days(dataset)
    with open(f'./tests/image_results/{__name__}.png', 'wb') as output:
        output.write(graph.getbuffer().tobytes())
    assert 'image' != 'image' # lol