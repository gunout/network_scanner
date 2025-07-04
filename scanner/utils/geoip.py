import geoip2.database
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

class GeoIPLocator:
    def __init__(self, db_path: str = 'GeoLite2-City.mmdb'):
        try:
            self.reader = geoip2.database.Reader(db_path)
        except FileNotFoundError:
            self.reader = None
            logger.warning("GeoIP database not found. Geo location disabled.")

    def locate_ip(self, ip: str) -> Optional[Dict]:
        """Get geographic location for an IP address"""
        if not self.reader:
            return None
            
        try:
            response = self.reader.city(ip)
            return {
                'country': response.country.name,
                'city': response.city.name,
                'latitude': response.location.latitude,
                'longitude': response.location.longitude
            }
        except Exception as e:
            logger.error(f"GeoIP lookup error: {e}")
            return None
