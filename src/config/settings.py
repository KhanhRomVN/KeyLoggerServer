import os
from pathlib import Path

def get_project_root():
    """Get the project root directory"""
    return Path(__file__).parent.parent.parent

def get_data_dir():
    """Get the data directory path"""
    return get_project_root() / "data"

def get_config_dir():
    """Get the config directory path"""
    return get_project_root() / "config"

def get_ssl_cert_path():
    """Get SSL certificate path"""
    return get_config_dir() / "ssl" / "server.crt"

def get_ssl_key_path():
    """Get SSL key path"""
    return get_config_dir() / "ssl" / "server.key"

def get_database_path():
    """Get database path"""
    return get_data_dir() / "database" / "keylogger.db"

def get_logs_path():
    """Get logs path"""
    return get_data_dir() / "logs" / "server.log"