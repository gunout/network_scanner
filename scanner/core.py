import socket
import requests
import dns.resolver
import concurrent.futures
from typing import List, Dict
import logging
from datetime import datetime

class NetworkScanner:
    def __init__(self, max_threads: int = 10):
        self.logger = self._setup_logger()
        self.max_threads = max_threads
        self.user_agent = "CyberpunkIPScanner/1.0"
        
    def _setup_logger(self):
        logger = logging.getLogger('CyberScanner')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def scan_website(self, url: str) -> Dict:
        """Scan complet d'un site web"""
        if not url.startswith(('http://', 'https://')):
            url = f'https://{url}'
            
        results = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'ip_info': self.get_ip_info(url),
            'dns_records': self.get_dns_records(url),
            'server_info': self.get_server_info(url),
            'open_ports': self.scan_ports(url)
        }
        
        return results

    def get_ip_info(self, url: str) -> Dict:
        """Récupère les informations IP de base"""
        try:
            domain = url.split('//')[-1].split('/')[0]
            ip = socket.gethostbyname(domain)
            
            return {
                'ip_address': ip,
                'reverse_dns': socket.getfqdn(ip),
                'is_up': self.check_host(ip)
            }
        except Exception as e:
            self.logger.error(f"IP scan error: {e}")
            return {'error': str(e)}

    def get_dns_records(self, url: str) -> Dict:
        """Récupère les enregistrements DNS"""
        domain = url.split('//')[-1].split('/')[0]
        records = {}
        
        try:
            # A Records
            answers = dns.resolver.resolve(domain, 'A')
            records['A'] = [str(r) for r in answers]
            
            # MX Records
            answers = dns.resolver.resolve(domain, 'MX')
            records['MX'] = [str(r.exchange) for r in answers]
            
            # NS Records
            answers = dns.resolver.resolve(domain, 'NS')
            records['NS'] = [str(r) for r in answers]
            
            # TXT Records
            answers = dns.resolver.resolve(domain, 'TXT')
            records['TXT'] = [str(r) for r in answers]
            
        except Exception as e:
            self.logger.error(f"DNS scan error: {e}")
            
        return records

    def scan_ports(self, url: str, ports: List[int] = None) -> Dict:
        """Scan des ports ouverts"""
        if ports is None:
            ports = [21, 22, 80, 443, 8080, 8443]
            
        domain = url.split('//')[-1].split('/')[0]
        ip = socket.gethostbyname(domain)
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            future_to_port = {executor.submit(self.check_port, ip, port): port for port in ports}
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    results[port] = future.result()
                except Exception as e:
                    results[port] = {'status': 'error', 'error': str(e)}
                    
        return results

    def check_port(self, ip: str, port: int) -> Dict:
        """Vérifie un port individuel"""
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

    def get_server_info(self, url: str) -> Dict:
        """Récupère les en-têtes HTTP du serveur"""
        try:
            response = requests.head(
                url, 
                headers={'User-Agent': self.user_agent},
                allow_redirects=True,
                timeout=5
            )
            
            return {
                'server': response.headers.get('Server'),
                'content_type': response.headers.get('Content-Type'),
                'security_headers': {
                    'strict_transport_security': response.headers.get('Strict-Transport-Security'),
                    'content_security_policy': response.headers.get('Content-Security-Policy'),
                    'x_frame_options': response.headers.get('X-Frame-Options')
                },
                'status_code': response.status_code,
                'final_url': response.url
            }
        except Exception as e:
            self.logger.error(f"Server info error: {e}")
            return {'error': str(e)}

    def check_host(self, ip: str) -> bool:
        """Vérifie si l'hôte est en ligne"""
        try:
            socket.create_connection((ip, 80), timeout=2)
            return True
        except:
            return False
