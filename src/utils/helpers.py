import os
import json
from datetime import datetime
from pathlib import Path

def ensure_directory_exists(path):
    """Ensure that a directory exists, create it if it doesn't"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path

def get_timestamp():
    """Get current timestamp in ISO format"""
    return datetime.utcnow().isoformat()

def validate_client_data(data):
    """Validate incoming client data structure"""
    required_fields = ['client_id']
    return all(field in data for field in required_fields)

def format_response(success, message, data=None):
    """Format a standardized API response"""
    response = {
        'success': success,
        'message': message,
        'timestamp': get_timestamp()
    }
    if data is not None:
        response['data'] = data
    return response

def save_debug_data(data_type, data, directory="debug"):
    """Save data for debugging purposes"""
    ensure_directory_exists(directory)
    filename = f"{data_type}_{get_timestamp().replace(':', '-')}.json"
    filepath = os.path.join(directory, filename)
    
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    
    return filepath