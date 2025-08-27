from flask import Flask
from flask_jwt_extended import JWTManager
from src.config.config_loader import load_config
from src.database.database import init_db
from src.api.routes import register_routes
from src.utils.logger import setup_logging
import os

def create_app():
    app = Flask(__name__)
    
    # Load configuration
    config = load_config()
    
    # Setup logging
    setup_logging(config)
    
    # Configure app
    app.config['JWT_SECRET_KEY'] = config['security']['jwt_secret']
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = config['security']['token_expiration']
    
    # Initialize extensions
    jwt = JWTManager(app)
    
    # Initialize database
    init_db(app, config)
    
    # Register routes
    register_routes(app)
    
    return app

app = create_app()

if __name__ == '__main__':
    config = load_config()
    ssl_context = (
        config['server']['ssl_cert'],
        config['server']['ssl_key']
    )
    app.run(
        host=config['server']['host'],
        port=config['server']['port'],
        debug=config['server']['debug'],
        ssl_context=ssl_context
    )