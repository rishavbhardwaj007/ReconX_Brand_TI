# utils/dns_enum.py

import socket
import requests
import json
import dns.resolver
import dns.exception
import os

def dns_enumeration(brand):
    """
    Perform DNS enumeration to find subdomains and DNS records
    """
    results = {
        'subdomains': [],
        'dns_records': {},
        'certificates': [],
        'exposed_services': []
    }

    domain = brand if '.' in brand else f"{brand}.com"

    # Find subdomains
    results['subdomains'] = find_subdomains(domain)

    # Get DNS records
    results['dns_records'] = get_dns_records(domain)

    # Check certificate transparency logs
    results['certificates'] = check_certificate_transparency(domain)

    # Check for exposed services
    results['exposed_services'] = check_exposed_services(domain)

    return results

def find_subdomains(domain):
    """
    Find subdomains using dictionary + crt.sh + ViewDNS
    """
    subdomains = []

    # Method 1: Common subdomain wordlist
    common_subdomains = [
        'www', 'mail', 'ftp', 'admin', 'api', 'dev', 'test', 'staging',
        'prod', 'portal', 'blog', 'shop', 'store', 'support', 'docs',
        'cdn', 'images', 'static', 'media', 'assets', 'vpn', 'ssh'
    ]

    for subdomain in common_subdomains:
        full_domain = f"{subdomain}.{domain}"
        try:
            ip = socket.gethostbyname(full_domain)
            subdomains.append({
                'subdomain': full_domain,
                'method': 'dictionary',
                'ip': ip
            })
        except socket.gaierror:
            pass

    # Method 2: Certificate Transparency
    subdomains.extend(get_subdomains_from_ct(domain))

    # Method 3: ViewDNS API
    subdomains.extend(get_subdomains_viewdns(domain))

    return subdomains

def get_dns_records(domain):
    """
    Get various DNS records for the domain
    """
    records = {}
    record_types = ['A', 'AAAA', 'MX', 'NS', 'TXT', 'CNAME', 'SOA']

    for record_type in record_types:
        try:
            answers = dns.resolver.resolve(domain, record_type)
            records[record_type] = [str(answer) for answer in answers]
        except dns.exception.DNSException:
            records[record_type] = []

    return records

def check_certificate_transparency(domain):
    """
    Check certificate transparency logs for certificates
    """
    certificates = []

    try:
        url = f"https://crt.sh/?q={domain}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            certs = response.json()
            for cert in certs[:10]:
                certificates.append({
                    'id': cert.get('id'),
                    'common_name': cert.get('common_name'),
                    'name_value': cert.get('name_value'),
                    'issuer_ca_id': cert.get('issuer_ca_id'),
                    'issuer_name': cert.get('issuer_name'),
                    'not_before': cert.get('not_before'),
                    'not_after': cert.get('not_after')
                })
    except Exception as e:
        print(f"Error checking certificate transparency: {e}")

    return certificates

def get_subdomains_from_ct(domain):
    """
    Extract subdomains from certificate transparency logs
    """
    subdomains = []

    try:
        url = f"https://crt.sh/?q=%.{domain}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            certs = response.json()
            unique = set()
            for cert in certs:
                for name in cert.get('name_value', '').split('\n'):
                    name = name.strip()
                    if name and domain in name and name not in unique:
                        unique.add(name)
                        try:
                            ip = socket.gethostbyname(name)
                            subdomains.append({
                                'subdomain': name,
                                'method': 'certificate_transparency',
                                'ip': ip
                            })
                        except socket.gaierror:
                            subdomains.append({
                                'subdomain': name,
                                'method': 'certificate_transparency',
                                'ip': 'N/A'
                            })
    except Exception as e:
        print(f"Error getting subdomains from CT: {e}")

    return subdomains

def get_subdomains_viewdns(domain):
    """
    Get subdomains using ViewDNS.info API
    """
    subdomains = []
    api_key = os.getenv('VIEWDNS_API_KEY')
    if not api_key:
        return []

    try:
        url = f"https://api.viewdns.info/subdomains/?domain={domain}&apikey={api_key}&output=json"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("subdomains", []):
                subdomains.append({
                    "subdomain": item['name'],
                    "method": "viewdns",
                    "ip": "N/A"
                })
    except Exception as e:
        print(f"Error using ViewDNS API: {e}")

    return subdomains

def check_exposed_services(domain):
    """
    Check for exposed services on the domain
    """
    services = []
    common_ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3389, 5432, 3306]

    try:
        ip = socket.gethostbyname(domain)
        for port in common_ports[:5]:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            result = sock.connect_ex((ip, port))
            if result == 0:
                service_name = socket.getservbyport(port) if port in [21, 22, 23, 25, 53, 80, 443] else 'unknown'
                services.append({
                    'ip': ip,
                    'port': port,
                    'service': service_name,
                    'status': 'open'
                })
            sock.close()
    except Exception as e:
        print(f"Error checking exposed services: {e}")

    return services
