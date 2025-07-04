import socket
import concurrent.futures
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

def scan_ports(ip: str, ports: List[int] = None, max_threads: int = 10) -> Dict:
    """Scan open ports on an IP address"""
    if ports is None:
        ports = [21, 22, 80, 443, 8080, 8443]
        
    results = {}
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        future_to_port = {executor.submit(check_port, ip, port): port for port in ports}
        for future in concurrent.futures.as_completed(future_to_port):
            port = future_to_port[future]
            try:
                results[port] = future.result()
            except Exception as e:
                results[port] = {'status': 'error', 'error': str(e)}
                
    return results

def check_port(ip: str, port: int) -> Dict:
    """Check individual port status"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1.0)
            result = s.connect_ex((ip, port))
            return {
                'status': 'open' if result == 0 else 'closed',
                'service': socket.getservbyport(port) if result == 0 else None
            }
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
