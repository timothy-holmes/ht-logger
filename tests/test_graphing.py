import matplotlib.image as mpimg

from src.config import config as CONFIG
print(__name__,CONFIG.sqlite_file_name)
from src.graphing import graph_n_days, get_n_days
from tests.ex_data import for_graph

# TODO: change sample data gathering to test database

def test_n_days():
    """Check if function returns non-empty object of correct type:
            dict( 
                str, 
                list( 
                    dict( 
                        str, 
                        int | float 
                    )
                )
            )
    """
    dataset = get_n_days(n_days = 3)
    assert type(outer_d := dataset) == 'dict'
    assert type(l := outer_d.get(outer_d.keys()[0])) == 'list'
    assert type(inner_d := l[0]) == 'list'
    assert (type(inner_d.get(inner_d.keys()[0])) == 'float') or \
           (type(inner_d.get(inner_d.keys()[0])) == 'int')

def test_graph_n_days():
    """
    Generate graph from last n days of data, and check if series has been plotted.

    Checks for a colour pixel at mid-width, eg. series line.
    """
    # generate graph
    dataset = {device_id: list(sorted(data,key = lambda d: d.get('d'))) for device_id, data in for_graph.items()}
    graph = graph_n_days(dataset)
    assert graph.__sizeof__() > 0

    # test for colour
    # with open(f'./tests/image_results/{__name__}.png', 'wb') as output:
    #     output.write(graph.getbuffer().tobytes())
    image = mpimg.imread(graph.getbuffer()) # maybe just `graph`
    assert image.shape[-1] >= 3 # 3 or more channels ie. RGB, RGBa

    half_width = image.shape[0] // 2
    is_colour_pixel = lambda p: not(p[0] == p[1] and p[1] == p[2])
    assert any(
        is_colour_pixel(image[half_width,i]) 
        for i in range(image.shape[1])
    )