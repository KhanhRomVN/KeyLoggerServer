import requests
from src.config.config_loader import load_config
from src.utils.encryption import encrypt_payload
import logging

logger = logging.getLogger(__name__)

class RemoteServer:
    def __init__(self):
        self.config = load_config()
        self.base_url = self.config.get('remote', 'base_url', fallback='')
        self.api_key = self.config.get('remote', 'api_key', fallback='')
        self.enabled = self.config.getboolean('remote', 'enabled', fallback=False)
    
    def forward_data(self, endpoint, data):
        """Forward data to remote server"""
        if not self.enabled or not self.base_url:
            return False
        
        try:
            url = f"{self.base_url}/{endpoint}"
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }
            
            # Encrypt data before sending if configured
            if self.config.getboolean('remote', 'encrypt_data', fallback=True):
                encrypted_data = encrypt_payload(data)
                payload = {'encrypted': True, 'data': encrypted_data}
            else:
                payload = data
            
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            logger.info(f"Data forwarded to remote server: {endpoint}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to forward data to remote server: {str(e)}")
            return False
    
    def sync_clients(self, clients_data):
        """Sync client information to remote server"""
        return self.forward_data('api/clients/sync', clients_data)
    
    def sync_logs(self, logs_data):
        """Sync logs to remote server"""
        return self.forward_data('api/logs/sync', logs_data)