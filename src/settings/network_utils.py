import socket
import requests
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

def check_internet_connection():
    """Check if internet connection is available"""
    try:
        # Try to connect to a reliable server
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        pass
    
    try:
        # Alternative check using requests
        response = requests.get("https://www.google.com", timeout=10)
        return response.status_code == 200
    except Exception:
        return False

def get_public_ip():
    """Get the public IP address of the server"""
    try:
        response = requests.get("https://api.ipify.org", timeout=10)
        return response.text.strip()
    except Exception:
        return "Unknown"

def is_valid_url(url):
    """Check if a URL is valid"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def get_client_ip(request):
    """Get the client IP address from the request"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers['X-Forwarded-For'].split(',')[0].strip()
    return request.remote_addr

def check_port_open(host, port, timeout=2):
    """Check if a port is open on a host"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return s.connect_ex((host, port)) == 0
    except Exception:
        return False