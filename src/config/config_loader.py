import configparser
import os
from pathlib import Path

def load_config():
    config = configparser.ConfigParser()
    config_path = Path('config/server_config.ini')
    
    if not config_path.exists():
        raise FileNotFoundError("Configuration file not found")
    
    config.read(config_path)
    
    # Strip inline comments from values
    for section in config.sections():
        for key in config[section]:
            value = config[section][key]
            if '#' in value:
                config[section][key] = value.split('#')[0].strip()
                
    return config