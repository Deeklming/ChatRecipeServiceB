import dotenv
from os import getenv as cfg

### env
def config_settings():
    _mode = cfg("YXSMODE", "dev")
    if _mode == 'dev':
        _dotenv_file = dotenv.find_dotenv(".env.dev")
        dotenv.load_dotenv(_dotenv_file)
    elif _mode == 'prod':
        _dotenv_file = dotenv.find_dotenv(".env.prod")
        dotenv.load_dotenv(_dotenv_file)
