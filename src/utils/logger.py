import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(config):
    log_level = getattr(logging, config['logging']['level'].upper())
    log_path = config['logging']['path']
    
    # Create log directory if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=config['logging'].getint('max_size'),
        backupCount=config['logging'].getint('backup_count')
    )
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)