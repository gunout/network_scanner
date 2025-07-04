import dns.resolver
from typing import Dict
import logging

logger = logging.getLogger(__name__)

def get_dns_records(domain: str) -> Dict:
    """Get DNS records for a domain"""
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
        logger.error(f"DNS scan error: {e}")
        
    return records
