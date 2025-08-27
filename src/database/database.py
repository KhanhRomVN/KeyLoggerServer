from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path

db = SQLAlchemy()

def init_db(app, config):
    database_path = config['database']['path']
    
    # Tạo thư mục chứa database nếu chưa tồn tại
    database_dir = os.path.dirname(database_path)
    if database_dir:  # Nếu có thư mục con
        os.makedirs(database_dir, exist_ok=True)
    
    # Đảm bảo đường dẫn tuyệt đối
    abs_database_path = os.path.abspath(database_path)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{abs_database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        if config['database'].getboolean('auto_create'):
            db.create_all()
            print(f"Database created at: {abs_database_path}")