import os.path

from src.config import ConfigData

class TestConfigData(ConfigData):
    # independent
    test_image_output_path: str = './tests/image_results'
    test_request_pickle_path: str = './tests/ex_data/req_pickles.pickle'
    data_volume_path: str = './tests/ex_data'
    sqlite_db_filename: str = "database.test.db"

class TestConfig(TestConfigData):
    # dependent
    sqlite_db_path: str = os.path.abspath(os.path.join(data_volume_path,sqlite_db_filename))
    sqlite_url: str = f"sqlite:///{sqlite_db_path}"

test_config = TestConfig()