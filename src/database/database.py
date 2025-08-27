from flask_sqlalchemy import SQLAlchemy
import os
from pathlib import Path

db = SQLAlchemy()

def init_db(app, config):
    database_path = config['database']['path']
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    with app.app_context():
        if config['database'].getboolean('auto_create'):
            db.create_all()