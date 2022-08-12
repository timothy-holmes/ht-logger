import matplotlib.image as mpimg
import pytest

from src.config import config as CONFIG
from src.graphing import graph_n_days, get_n_days

# TODO: change sample data gathering to test database

@pytest.mark.asyncio
async def test_graph_n_days(engine):
    """
    Generate graph from last n days of data, and check if series has been plotted.

    Checks for a colour pixel at mid-width, eg. series line.
    """
    # generate graph
    dataset = await get_n_days(n_days = 3, engine = engine)
    graph = await graph_n_days(dataset)
    assert graph.__sizeof__() > 0

    with open(CONFIG.test_image_output_path, 'wb') as output:
        output.write(graph.getbuffer().tobytes())
    image = mpimg.imread(graph) # maybe just `graph`
    assert image.shape[-1] >= 3 # 3 or more channels ie. RGB, RGBa

    half_width = image.shape[0] // 2
    is_colour_pixel = lambda p: not(p[0] == p[1] and p[1] == p[2])
    assert any(
        is_colour_pixel(image[half_width,i]) 
        for i in range(image.shape[1])
    )