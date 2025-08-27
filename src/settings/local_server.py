import socket
from src.config.settings import get_project_root
from src.utils.helpers import ensure_directory_exists
import logging

logger = logging.getLogger(__name__)

class LocalNetworkServer:
    def __init__(self):
        self.local_ip = self.get_local_ip()
        self.base_path = get_project_root() / "local_data"
        ensure_directory_exists(self.base_path)
    
    def get_local_ip(self):
        """Get the local IP address of the server"""
        try:
            # Create a socket connection to get the local IP
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception:
            return "127.0.0.1"
    
    def save_local_data(self, data_type, client_id, data):
        """Save data locally for LAN clients"""
        try:
            client_dir = self.base_path / client_id / data_type
            ensure_directory_exists(client_dir)
            
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{data_type}_{timestamp}.json"
            filepath = client_dir / filename
            
            import json
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.debug(f"Data saved locally: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save local data: {str(e)}")
            return False
    
    def is_local_client(self, client_ip):
        """Check if client is on local network"""
        try:
            # Simple check: see if client IP is in same subnet
            server_octets = self.local_ip.split('.')
            client_octets = client_ip.split('.')
            
            return server_octets[0] == client_octets[0] and \
                   server_octets[1] == client_octets[1] and \
                   server_octets[2] == client_octets[2]
                   
        except Exception:
            return False