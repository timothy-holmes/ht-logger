from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.graphing import graph_n_days
from tests.ex_data import for_graph

def test_graph_n_days():
    dataset = {device_id: list(sorted(data,key = lambda d: d.get('d'))) for device_id, data in for_graph.items()}
    graph = graph_n_days(dataset)
    with open(f'./tests/image_results/{__name__}.png', 'wb') as output:
        output.write(graph.getbuffer().tobytes())
    assert 'image' != 'image' # lol