import configparser
import os
from pathlib import Path

def load_config():
    config = configparser.ConfigParser()
    config_path = Path('config/server_config.ini')
    
    if not config_path.exists():
        raise FileNotFoundError("Configuration file not found")
    
    config.read(config_path)
    return config