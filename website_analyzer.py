"""
Website analysis module for detecting platform, booking systems, and quality signals
"""
import re
import requests
from typing import Dict, Optional, Tuple
from urllib.parse import urlparse
import time


class WebsiteAnalyzer:
    """Analyzes business websites for lead quality signals"""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def analyze(self, website_url: str) -> Dict:
        """
        Analyze a website and extract quality signals
        
        Args:
            website_url: URL of the website to analyze
            
        Returns:
            Dictionary with analysis results
        """
        if not website_url or not website_url.strip():
            return self._empty_analysis()
        
        # Normalize URL
        url = website_url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            html_content = response.text
            final_url = response.url
            
            analysis = {
                "has_https": final_url.startswith('https://'),
                "status_code": response.status_code,
                "platform": self._detect_platform(html_content, final_url),
                "has_online_booking": self._detect_booking_system(html_content),
                "is_weak_website": self._detect_weak_website(html_content),
                "has_contact_form": self._detect_contact_form(html_content),
                "has_whatsapp": self._detect_whatsapp(html_content),
                "word_count": len(html_content.split()),
            }
            
            return analysis
            
        except requests.exceptions.RequestException as e:
            return {
                "error": str(e),
                "has_https": False,
                "platform": "unknown",
                "has_online_booking": False,
                "is_weak_website": True,  # If we can't access, assume weak
            }
        except Exception as e:
            return {
                "error": str(e),
                "has_https": False,
                "platform": "unknown",
                "has_online_booking": False,
                "is_weak_website": True,
            }
    
    def _detect_platform(self, html: str, url: str) -> str:
        """Detect the CMS/platform used"""
        html_lower = html.lower()
        
        # Check for platform indicators
        if 'powered by wix' in html_lower or 'wix.com' in html_lower:
            return "Wix"
        if 'wordpress' in html_lower or '/wp-content/' in html_lower:
            return "WordPress"
        if 'shopify' in html_lower or '.myshopify.com' in url:
            return "Shopify"
        if 'squarespace' in html_lower:
            return "Squarespace"
        if 'weebly' in html_lower:
            return "Weebly"
        if 'godaddy' in html_lower or 'godaddy.com' in url:
            return "GoDaddy Website Builder"
        if 'jimdo' in html_lower:
            return "Jimdo"
        if 'joomla' in html_lower:
            return "Joomla"
        if 'drupal' in html_lower:
            return "Drupal"
        
        return "Custom/Unknown"
    
    def _detect_booking_system(self, html: str) -> bool:
        """Detect if website has online booking system"""
        html_lower = html.lower()
        
        booking_indicators = [
            'book now',
            'book appointment',
            'schedule appointment',
            'online booking',
            'reserve table',
            'calendly',
            'acuity scheduling',
            'bookeo',
            'reservio',
            'timetap',
            'booking widget',
            'appointment booking',
            'reservation system',
        ]
        
        for indicator in booking_indicators:
            if indicator in html_lower:
                return True
        
        # Check for common booking widget scripts
        if re.search(r'(calendly|acuity|bookeo|reservio)', html_lower):
            return True
        
        return False
    
    def _detect_contact_form(self, html: str) -> bool:
        """Detect if website has contact form"""
        html_lower = html.lower()
        
        form_indicators = [
            '<form',
            'contact-form',
            'wpcf7',  # Contact Form 7 (WordPress)
            'gravityforms',
            'ninja-forms',
        ]
        
        for indicator in form_indicators:
            if indicator in html_lower:
                return True
        
        return False
    
    def _detect_whatsapp(self, html: str) -> bool:
        """Detect if website has WhatsApp contact"""
        html_lower = html.lower()
        
        whatsapp_indicators = [
            'wa.me',
            'whatsapp',
            'whats-app',
            'api.whatsapp.com',
        ]
        
        for indicator in whatsapp_indicators:
            if indicator in html_lower:
                return True
        
        return False
    
    def _detect_weak_website(self, html: str) -> bool:
        """Detect if website appears weak/outdated"""
        html_lower = html.lower()
        word_count = len(html.split())
        
        # Very short content
        if word_count < 100:
            return True
        
        # Common weak website indicators
        weak_indicators = [
            'under construction',
            'coming soon',
            'website by',
            'powered by',
            'template',
            'free website',
        ]
        
        weak_count = sum(1 for indicator in weak_indicators if indicator in html_lower)
        
        # Too many weak indicators
        if weak_count >= 3:
            return True
        
        return False
    
    def _empty_analysis(self) -> Dict:
        """Return empty analysis structure"""
        return {
            "has_https": False,
            "platform": "none",
            "has_online_booking": False,
            "is_weak_website": True,
            "has_contact_form": False,
            "has_whatsapp": False,
            "word_count": 0,
        }
    
    def extract_email(self, html: str) -> Optional[str]:
        """Extract email addresses from HTML"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, html)
        
        # Filter out common false positives
        filtered = [
            e for e in emails
            if not any(exclude in e.lower() for exclude in ['example.com', 'test.com', 'placeholder'])
        ]
        
        return filtered[0] if filtered else None

