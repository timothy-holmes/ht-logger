import os.path

from src.config import ConfigData

class TestConfigData(ConfigData):
    # independent
    test_image_output_path: str = './tests/image_results/output.png'
    test_request_pickle_path: str = './tests/ex_data/req_pickles.pickle'
    data_volume_path: str = './tests/ex_data'
    sqlite_db_filename: str = "database.test.db"

class TestConfig(TestConfigData):
    # dependent
    def __init__(cls):
        cls.sqlite_db_path: str = os.path.abspath(os.path.join(cls.data_volume_path,cls.sqlite_db_filename))
        cls.sqlite_url: str = f"sqlite:///{cls.sqlite_db_path}"

test_config = TestConfig()