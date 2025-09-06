"""
EML File Parser for Advanced Email Analysis
Extracts ALL data from .eml files including hidden links, headers, metadata
"""
import email
from email.header import decode_header
import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import base64

class EMLParser:
    def __init__(self):
        self.suspicious_domains = [
            'bit.ly', 'tinyurl.com', 'shorturl.at', 't.co', 
            'rebrand.ly', 'ow.ly', 'buff.ly', 'short.link'
        ]
        self.suspicious_keywords = [
            'urgent', 'verify', 'suspend', 'expire', 'click here',
            'act now', 'limited time', 'congratulations', 'winner',
            'free money', 'inheritance', 'lottery', 'prince',
            'nigeria', 'million dollars', 'tax refund'
        ]

    def parse_eml_file(self, eml_content):
        """Parse .eml file and extract comprehensive features"""
        try:
            # Parse email message
            msg = email.message_from_string(eml_content)
            
            # Extract basic headers
            features = self._extract_headers(msg)
            
            # Extract body content and links
            body_features = self._extract_body_content(msg)
            features.update(body_features)
            
            # Extract security indicators
            security_features = self._extract_security_features(msg)
            features.update(security_features)
            
            # Extract hidden/embedded content
            hidden_features = self._extract_hidden_content(msg)
            features.update(hidden_features)
            
            return features
            
        except Exception as e:
            print(f"Error parsing EML: {e}")
            return {"error": str(e)}

    def _extract_headers(self, msg):
        """Extract and analyze email headers"""
        features = {}
        
        # Basic headers
        features['from'] = self._decode_header(msg.get('From', ''))
        features['to'] = self._decode_header(msg.get('To', ''))
        features['subject'] = self._decode_header(msg.get('Subject', ''))
        features['date'] = msg.get('Date', '')
        
        # Security headers
        features['spf'] = msg.get('Received-SPF', 'none')
        features['dkim'] = msg.get('DKIM-Signature', 'none')
        features['dmarc'] = msg.get('Authentication-Results', 'none')
        
        # Routing headers
        received_headers = msg.get_all('Received') or []
        features['received_count'] = len(received_headers)
        features['received_hops'] = self._analyze_received_headers(received_headers)
        
        # Suspicious header patterns
        features['suspicious_from'] = self._check_suspicious_sender(features['from'])
        features['subject_urgency'] = self._check_subject_urgency(features['subject'])
        
        return features

    def _extract_body_content(self, msg):
        """Extract and analyze email body content"""
        features = {}
        
        # Get plain text and HTML content
        plain_text = ""
        html_content = ""
        
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    plain_text += part.get_payload(decode=True).decode('utf-8', errors='ignore')
                elif content_type == "text/html":
                    html_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        else:
            content_type = msg.get_content_type()
            payload = msg.get_payload(decode=True)
            if payload:
                content = payload.decode('utf-8', errors='ignore')
                if content_type == "text/plain":
                    plain_text = content
                elif content_type == "text/html":
                    html_content = content

        features['plain_text'] = plain_text
        features['html_content'] = html_content
        
        # Analyze content
        features['text_length'] = len(plain_text)
        features['html_length'] = len(html_content)
        features['has_html'] = len(html_content) > 0
        
        # Extract and analyze links
        links = self._extract_all_links(plain_text, html_content)
        features['links'] = links
        features['link_analysis'] = self._analyze_links(links)
        
        # Keyword analysis
        features['suspicious_keywords'] = self._count_suspicious_keywords(plain_text + html_content)
        
        return features

    def _extract_security_features(self, msg):
        """Extract security-related features"""
        features = {}
        
        # SPF record analysis
        spf = msg.get('Received-SPF', '').lower()
        features['spf_pass'] = 'pass' in spf
        features['spf_fail'] = 'fail' in spf
        
        # DKIM analysis
        dkim = msg.get('DKIM-Signature', '')
        features['has_dkim'] = len(dkim) > 0
        
        # Return-Path vs From mismatch
        return_path = msg.get('Return-Path', '')
        from_addr = msg.get('From', '')
        features['return_path_mismatch'] = self._check_address_mismatch(return_path, from_addr)
        
        # Message-ID analysis
        message_id = msg.get('Message-ID', '')
        features['suspicious_message_id'] = self._check_suspicious_message_id(message_id)
        
        return features

    def _extract_hidden_content(self, msg):
        """Extract hidden/embedded content that copy-paste misses"""
        features = {}
        
        # Get HTML content for hidden link analysis
        html_content = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/html":
                    html_content += part.get_payload(decode=True).decode('utf-8', errors='ignore')
        
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find hidden links in buttons, images, etc.
            hidden_links = []
            
            # Links in buttons
            buttons = soup.find_all(['button', 'input'])
            for button in buttons:
                onclick = button.get('onclick', '')
                if 'location' in onclick or 'window.open' in onclick:
                    hidden_links.append(onclick)
            
            # Links in JavaScript
            scripts = soup.find_all('script')
            for script in scripts:
                if script.string:
                    # Extract URLs from JavaScript
                    js_urls = re.findall(r'https?://[^\s"\']+', script.string)
                    hidden_links.extend(js_urls)
            
            # CSS hidden elements with links
            styles = soup.find_all('style')
            for style in styles:
                if style.string:
                    css_urls = re.findall(r'url\(["\']?(https?://[^"\')\s]+)', style.string)
                    hidden_links.extend(css_urls)
            
            # Meta refresh redirects
            meta_refresh = soup.find_all('meta', {'http-equiv': 'refresh'})
            for meta in meta_refresh:
                content = meta.get('content', '')
                if 'url=' in content:
                    redirect_url = content.split('url=')[1]
                    hidden_links.append(redirect_url)
            
            features['hidden_links'] = hidden_links
            features['hidden_link_count'] = len(hidden_links)
            features['has_javascript_redirects'] = any('location' in link or 'window.open' in link for link in hidden_links)
            
            # Check for obfuscated content
            features['has_base64_content'] = 'base64' in html_content.lower()
            features['suspicious_css'] = self._check_suspicious_css(html_content)
        
        return features

    def _extract_all_links(self, plain_text, html_content):
        """Extract all links from both plain text and HTML"""
        links = []
        
        # Extract from plain text
        plain_links = re.findall(r'https?://[^\s]+', plain_text)
        links.extend(plain_links)
        
        # Extract from HTML
        if html_content:
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Regular <a> tags
            a_tags = soup.find_all('a', href=True)
            for a in a_tags:
                links.append(a['href'])
            
            # Image links
            img_tags = soup.find_all('img', src=True)
            for img in img_tags:
                if img['src'].startswith('http'):
                    links.append(img['src'])
            
            # Form actions
            forms = soup.find_all('form', action=True)
            for form in forms:
                if form['action'].startswith('http'):
                    links.append(form['action'])
        
        return list(set(links))  # Remove duplicates

    def _analyze_links(self, links):
        """Analyze extracted links for suspicious patterns"""
        analysis = {
            'total_links': len(links),
            'suspicious_domains': 0,
            'shortened_urls': 0,
            'ip_addresses': 0,
            'http_not_https': 0,
            'suspicious_tlds': 0,
            'phishing_keywords': 0
        }
        
        suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.pw', '.top', '.click']
        phishing_keywords = ['verify', 'secure', 'update', 'confirm', 'login', 'account']
        
        for link in links:
            try:
                parsed = urlparse(link)
                domain = parsed.netloc.lower()
                
                # Check for suspicious domains
                if any(sus_domain in domain for sus_domain in self.suspicious_domains):
                    analysis['shortened_urls'] += 1
                
                # Check for IP addresses
                if re.match(r'^\d+\.\d+\.\d+\.\d+', domain):
                    analysis['ip_addresses'] += 1
                
                # Check protocol
                if parsed.scheme == 'http':
                    analysis['http_not_https'] += 1
                
                # Check TLD
                if any(tld in domain for tld in suspicious_tlds):
                    analysis['suspicious_tlds'] += 1
                
                # Check for phishing keywords in URL
                if any(keyword in link.lower() for keyword in phishing_keywords):
                    analysis['phishing_keywords'] += 1
                    
            except Exception:
                continue
        
        return analysis

    def _decode_header(self, header):
        """Decode email header properly"""
        if not header:
            return ""
        
        decoded_parts = []
        for part, encoding in decode_header(header):
            if isinstance(part, bytes):
                decoded_parts.append(part.decode(encoding or 'utf-8', errors='ignore'))
            else:
                decoded_parts.append(str(part))
        
        return ''.join(decoded_parts)

    def _analyze_received_headers(self, received_headers):
        """Analyze email routing path"""
        if not received_headers:
            return {'hops': 0, 'suspicious': False}
        
        # Simple analysis - more hops might indicate forwarding/relaying
        hop_count = len(received_headers)
        suspicious = hop_count > 5  # Arbitrary threshold
        
        return {'hops': hop_count, 'suspicious': suspicious}

    def _check_suspicious_sender(self, from_addr):
        """Check if sender address looks suspicious"""
        if not from_addr:
            return False
        
        from_lower = from_addr.lower()
        
        # Check for suspicious patterns
        suspicious_patterns = [
            'noreply', 'no-reply', 'donotreply', 'auto@', 'system@',
            'admin@', 'support@', 'security@', 'billing@'
        ]
        
        return any(pattern in from_lower for pattern in suspicious_patterns)

    def _check_subject_urgency(self, subject):
        """Check subject for urgency indicators"""
        if not subject:
            return False
        
        urgency_words = [
            'urgent', 'immediate', 'asap', 'expires', 'deadline',
            'act now', 'limited time', 'hurry', 'expires today'
        ]
        
        subject_lower = subject.lower()
        return any(word in subject_lower for word in urgency_words)

    def _check_address_mismatch(self, return_path, from_addr):
        """Check if Return-Path and From address domains differ"""
        if not return_path or not from_addr:
            return False
        
        try:
            return_domain = re.search(r'@([^>]+)', return_path)
            from_domain = re.search(r'@([^>]+)', from_addr)
            
            if return_domain and from_domain:
                return return_domain.group(1).lower() != from_domain.group(1).lower()
        except Exception:
            pass
        
        return False

    def _check_suspicious_message_id(self, message_id):
        """Check Message-ID for suspicious patterns"""
        if not message_id:
            return True  # Missing Message-ID is suspicious
        
        # Check for random/generated looking IDs
        random_pattern = re.search(r'[a-f0-9]{20,}', message_id.lower())
        return bool(random_pattern)

    def _count_suspicious_keywords(self, content):
        """Count suspicious keywords in content"""
        if not content:
            return 0
        
        content_lower = content.lower()
        count = 0
        
        for keyword in self.suspicious_keywords:
            count += content_lower.count(keyword)
        
        return count

    def _check_suspicious_css(self, html_content):
        """Check for suspicious CSS patterns"""
        if not html_content:
            return False
        
        suspicious_css = [
            'display:none', 'visibility:hidden', 'opacity:0',
            'font-size:0', 'color:transparent', 'position:absolute'
        ]
        
        html_lower = html_content.lower()
        return any(css in html_lower for css in suspicious_css)

    def extract_features_for_ml(self, eml_content):
        """Extract features suitable for ML model training"""
        parsed_data = self.parse_eml_file(eml_content)
        
        if "error" in parsed_data:
            return None
        
        # Create feature vector for ML
        features = {
            # Text content
            'text': parsed_data.get('plain_text', '') + ' ' + parsed_data.get('subject', ''),
            'sender': parsed_data.get('from', ''),
            'spf_record': 'pass' if parsed_data.get('spf_pass', False) else 'fail',
            
            # Advanced features
            'link_count': parsed_data.get('link_analysis', {}).get('total_links', 0),
            'suspicious_links': (
                parsed_data.get('link_analysis', {}).get('shortened_urls', 0) +
                parsed_data.get('link_analysis', {}).get('ip_addresses', 0) +
                parsed_data.get('link_analysis', {}).get('suspicious_tlds', 0)
            ),
            'hidden_links': parsed_data.get('hidden_link_count', 0),
            'suspicious_keywords': parsed_data.get('suspicious_keywords', 0),
            'has_html': parsed_data.get('has_html', False),
            'spf_fail': parsed_data.get('spf_fail', False),
            'return_path_mismatch': parsed_data.get('return_path_mismatch', False),
            'suspicious_sender': parsed_data.get('suspicious_sender', False),
            'subject_urgency': parsed_data.get('subject_urgency', False),
            'received_hops': parsed_data.get('received_hops', {}).get('hops', 0),
            'has_javascript_redirects': parsed_data.get('has_javascript_redirects', False),
            'suspicious_css': parsed_data.get('suspicious_css', False)
        }
        
        return features
