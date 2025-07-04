import socket
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def get_ip_info(domain: str) -> Dict:
    """Get basic IP information for a domain"""
    try:
        ip = socket.gethostbyname(domain)
        return {
            'ip_address': ip,
            'reverse_dns': socket.getfqdn(ip),
            'is_up': check_host(ip)
        }
    except Exception as e:
        logger.error(f"IP scan error: {e}")
        return {'error': str(e)}

def check_host(ip: str) -> bool:
    """Check if host is online"""
    try:
        socket.create_connection((ip, 80), timeout=2)
        return True
    except:
        return False
