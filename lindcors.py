#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║  ██╗     ██╗███╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗
║  ██║     ██║████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║
║  ██║     ██║██╔██╗ ██║██║  ██║███████╗██║   ██║██████╔╝███████╗██║     ███████║██╔██╗ ██║
║  ██║     ██║██║╚██╗██║██║  ██║╚════██║██║   ██║██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║
║  ███████╗██║██║ ╚████║██████╔╝███████║╚██████╔╝██║  ██║███████║╚██████╗██║  ██║██║ ╚████║
║  ╚══════╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝
║                                    CORS MISCONFIGURATION SCANNER
║                                         by Lindan Tri Saputra
╚═══════════════════════════════════════════════════════════════╝
"""

import requests
import argparse
import sys
import time
import json
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import threading

# Colors for output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    DARK_RED = '\033[31m'
    DARK_GREEN = '\033[32m'
    DARK_YELLOW = '\033[33m'
    DARK_BLUE = '\033[34m'
    DARK_MAGENTA = '\033[35m'
    DARK_CYAN = '\033[36m'

# ASCII Art Logo
LOGO = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════════════════════╗
{Colors.RED}║{Colors.CYAN}        ██╗     ██╗███╗   ██╗██████╗ ███████╗ ██████╗ ██████╗ ███████╗ ██████╗ █████╗ ███╗   ██╗{Colors.RED}        ║
{Colors.RED}║{Colors.CYAN}        ██║     ██║████╗  ██║██╔══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔════╝██╔══██╗████╗  ██║{Colors.RED}        ║
{Colors.RED}║{Colors.CYAN}        ██║     ██║██╔██╗ ██║██║  ██║███████╗██║   ██║██████╔╝███████╗██║     ███████║██╔██╗ ██║{Colors.RED}        ║
{Colors.RED}║{Colors.CYAN}        ██║     ██║██║╚██╗██║██║  ██║╚════██║██║   ██║██╔══██╗╚════██║██║     ██╔══██║██║╚██╗██║{Colors.RED}        ║
{Colors.RED}║{Colors.CYAN}        ███████╗██║██║ ╚████║██████╔╝███████║╚██████╔╝██║  ██║███████║╚██████╗██║  ██║██║ ╚████║{Colors.RED}        ║
{Colors.RED}║{Colors.CYAN}        ╚══════╝╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝{Colors.RED}        ║
{Colors.RED}║{Colors.YELLOW}                         ███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗{Colors.RED}                  ║
{Colors.RED}║{Colors.YELLOW}                         ██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗{Colors.RED}                  ║
{Colors.RED}║{Colors.YELLOW}                         ███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝{Colors.RED}                  ║
{Colors.RED}║{Colors.YELLOW}                         ╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗{Colors.RED}                  ║
{Colors.RED}║{Colors.YELLOW}                         ███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║{Colors.RED}                  ║
{Colors.RED}║{Colors.YELLOW}                         ╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝{Colors.RED}                  ║
{Colors.RED}║{Colors.WHITE}                                 ┌─┐┬ ┬┌┐┌┌┬┐┬┌┐┌┌─┐┬ ┬┌─┐┬─┐{Colors.RED}                                      ║
{Colors.RED}║{Colors.WHITE}                                 │  └┬┘│││ │ ││││├┤ │ ││ │├┬┘{Colors.RED}                                      ║
{Colors.RED}║{Colors.WHITE}                                 └─┘ ┴ ┘└┘ ┴ ┴┘└┘└  └─┘└─┘┴└─{Colors.RED}                                      ║
{Colors.RED}║{Colors.GREEN}                                    CORS Misconfiguration Scanner v2.0{Colors.RED}                                 ║
{Colors.RED}║{Colors.MAGENTA}                                         by Lindan Tri Saputra{Colors.RED}                                         ║
{Colors.RED}╚═══════════════════════════════════════════════════════════════════════════════╝{Colors.END}
"""

class CORSScanner:
    def __init__(self, threads=10, timeout=5, output_file=None):
        self.threads = threads
        self.timeout = timeout
        self.output_file = output_file
        self.results = []
        self.lock = threading.Lock()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        })
        
    def print_banner(self):
        """Print the awesome banner"""
        print(LOGO)
        print(f"{Colors.CYAN}[*] CORS Misconfiguration Scanner initialized{Colors.END}")
        print(f"{Colors.CYAN}[*] Threads: {self.threads} | Timeout: {self.timeout}s{Colors.END}")
        print(f"{Colors.CYAN}[*] Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.END}")
        print(f"{Colors.RED}{'═'*80}{Colors.END}\n")

    def normalize_url(self, url):
        """Normalize URL to proper format"""
        url = url.strip()
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        return url.rstrip('/')

    def check_cors(self, url):
        """Check CORS misconfiguration for a single URL"""
        url = self.normalize_url(url)
        parsed = urlparse(url)
        domain = parsed.netloc
        
        # Test origins
        test_origins = [
            'https://evil.com',
            'https://evilsite.com',
            'https://evil.com.attacker.com',
            'https://attacker.com.evil.com',
            'https://subdomain.evil.com',
            'http://evil.com',
            'null',
            'https://evil.com:8080',
            'https://evil.com.evil.com',
            'https://evil.com.evil.com.evil.com',
            'https://evilsite.com',
            'https://evil.com@evil.com',
            'https://evil.com#evil.com',
        ]
        
        results = []
        
        try:
            # First, make a normal request to check if site is alive
            normal_response = self.session.get(url, timeout=self.timeout, verify=False)
            
            if normal_response.status_code >= 400:
                return {
                    'url': url,
                    'vulnerable': False,
                    'status': normal_response.status_code,
                    'reason': 'Site returned error status',
                    'details': []
                }
            
            # Get original ACAO header if present
            original_acao = normal_response.headers.get('Access-Control-Allow-Origin', 'Not Set')
            original_allow_credentials = normal_response.headers.get('Access-Control-Allow-Credentials', 'Not Set')
            
            # Test each origin
            for origin in test_origins:
                try:
                    headers = {
                        'Origin': origin,
                        'Referer': origin
                    }
                    
                    response = self.session.get(
                        url, 
                        headers=headers, 
                        timeout=self.timeout,
                        verify=False
                    )
                    
                    acao = response.headers.get('Access-Control-Allow-Origin', '')
                    allow_credentials = response.headers.get('Access-Control-Allow-Credentials', '')
                    exposed_headers = response.headers.get('Access-Control-Expose-Headers', '')
                    max_age = response.headers.get('Access-Control-Max-Age', '')
                    
                    is_vulnerable = False
                    severity = 'INFO'
                    message = ''
                    
                    # Check for misconfigurations
                    if acao == '*':
                        if allow_credentials.lower() == 'true':
                            is_vulnerable = True
                            severity = 'CRITICAL'
                            message = 'Wildcard origin (*) with credentials! This is a severe vulnerability.'
                        else:
                            is_vulnerable = True
                            severity = 'HIGH'
                            message = 'Wildcard origin (*) allows any domain. This is dangerous.'
                    
                    elif acao == origin:
                        is_vulnerable = True
                        severity = 'HIGH'
                        message = f'Reflects any origin. ACAO echoes the Origin header value.'
                        
                        if allow_credentials.lower() == 'true':
                            severity = 'CRITICAL'
                            message += ' Credentials are allowed!'
                    
                    elif acao == 'null':
                        is_vulnerable = True
                        severity = 'MEDIUM'
                        message = 'ACAO set to "null" which can be spoofed in sandboxed iframes.'
                    
                    elif acao and origin in acao:
                        is_vulnerable = True
                        severity = 'MEDIUM'
                        message = f'ACAO contains origin partially: {acao}'
                    
                    if is_vulnerable:
                        result = {
                            'origin': origin,
                            'acao': acao,
                            'allow_credentials': allow_credentials,
                            'exposed_headers': exposed_headers,
                            'max_age': max_age,
                            'status_code': response.status_code,
                            'severity': severity,
                            'message': message,
                            'original_acao': original_acao
                        }
                        results.append(result)
                        
                except requests.exceptions.Timeout:
                    continue
                except requests.exceptions.ConnectionError:
                    continue
                except Exception as e:
                    continue
                    
            return {
                'url': url,
                'vulnerable': len(results) > 0,
                'status': normal_response.status_code,
                'server': normal_response.headers.get('Server', 'Unknown'),
                'original_acao': original_acao,
                'original_credentials': original_allow_credentials,
                'details': results
            }
            
        except requests.exceptions.Timeout:
            return {'url': url, 'vulnerable': False, 'status': 'Timeout', 'error': True}
        except requests.exceptions.ConnectionError:
            return {'url': url, 'vulnerable': False, 'status': 'Connection Error', 'error': True}
        except Exception as e:
            return {'url': url, 'vulnerable': False, 'status': 'Error', 'error': True}

    def scan_single(self, url):
        """Scan single URL"""
        print(f"{Colors.CYAN}[*] Scanning: {Colors.WHITE}{url}{Colors.END}")
        result = self.check_cors(url)
        
        if result.get('error'):
            print(f"{Colors.RED}[!] Error scanning {url}: {result['status']}{Colors.END}")
        elif result['vulnerable']:
            self.print_vulnerable(result)
            with self.lock:
                self.results.append(result)
        else:
            print(f"{Colors.GREEN}[✓] {url} - Not vulnerable{Colors.END}")
            
        return result

    def scan_multi(self, file_path):
        """Scan multiple URLs from file"""
        try:
            with open(file_path, 'r') as f:
                urls = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"{Colors.RED}[!] Error reading file: {e}{Colors.END}")
            return
        
        print(f"{Colors.YELLOW}[*] Loaded {len(urls)} targets from {file_path}{Colors.END}")
        print(f"{Colors.YELLOW}[*] Starting scan with {self.threads} threads{Colors.END}\n")
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_cors, url): url for url in urls}
            
            for i, future in enumerate(as_completed(futures), 1):
                url = futures[future]
                try:
                    result = future.result()
                    if result.get('error'):
                        print(f"{Colors.RED}[!] [{i}/{len(urls)}] Error: {url} - {result['status']}{Colors.END}")
                    elif result['vulnerable']:
                        self.print_vulnerable(result)
                        with self.lock:
                            self.results.append(result)
                    else:
                        print(f"{Colors.GREEN}[✓] [{i}/{len(urls)}] {url} - Not vulnerable{Colors.END}")
                except Exception as e:
                    print(f"{Colors.RED}[!] [{i}/{len(urls)}] Exception for {url}: {e}{Colors.END}")

    def print_vulnerable(self, result):
        """Print vulnerable result in formatted way"""
        url = result['url']
        details = result['details']
        
        print(f"\n{Colors.RED}╔{'═'*78}╗{Colors.END}")
        print(f"{Colors.RED}║ {Colors.BOLD}🔥 VULNERABLE: {Colors.WHITE}{url}{Colors.END}{Colors.RED}{' '*(54-len(url))}║{Colors.END}")
        print(f"{Colors.RED}╠{'═'*78}╣{Colors.END}")
        
        for d in details:
            severity_color = {
                'CRITICAL': Colors.RED,
                'HIGH': Colors.YELLOW,
                'MEDIUM': Colors.MAGENTA,
                'LOW': Colors.BLUE,
                'INFO': Colors.CYAN
            }.get(d['severity'], Colors.WHITE)
            
            print(f"{Colors.RED}║ {severity_color}[{d['severity']}]{Colors.END} Origin: {Colors.CYAN}{d['origin']}{Colors.END}")
            print(f"{Colors.RED}║    ACAO: {Colors.GREEN}{d['acao']}{Colors.END}")
            print(f"{Colors.RED}║    Credentials: {Colors.YELLOW}{d['allow_credentials']}{Colors.END}")
            print(f"{Colors.RED}║    Message: {Colors.WHITE}{d['message']}{Colors.END}")
            print(f"{Colors.RED}║    Status: {Colors.MAGENTA}{d['status_code']}{Colors.END}")
            print(f"{Colors.RED}║{'─'*78}║{Colors.END}")
            
        print(f"{Colors.RED}╚{'═'*78}╝{Colors.END}\n")

    def generate_report(self):
        """Generate detailed report"""
        if not self.results:
            print(f"{Colors.YELLOW}[!] No vulnerabilities found to report{Colors.END}")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"cors_report_{timestamp}.txt"
        json_file = f"cors_report_{timestamp}.json"
        
        # Text report
        with open(report_file, 'w') as f:
            f.write("="*80 + "\n")
            f.write("LINDSCORSCAN - CORS MISCONFIGURATION REPORT\n")
            f.write(f"Generated by Lindan Tri Saputra\n")
            f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            critical = [r for r in self.results if any(d['severity'] == 'CRITICAL' for d in r['details'])]
            high = [r for r in self.results if any(d['severity'] == 'HIGH' for d in r['details'])]
            medium = [r for r in self.results if any(d['severity'] == 'MEDIUM' for d in r['details'])]
            
            f.write(f"SUMMARY:\n")
            f.write(f"  Total Vulnerable: {len(self.results)}\n")
            f.write(f"  Critical: {len(critical)}\n")
            f.write(f"  High: {len(high)}\n")
            f.write(f"  Medium: {len(medium)}\n\n")
            
            for i, result in enumerate(self.results, 1):
                f.write(f"[{i}] {result['url']}\n")
                f.write(f"  Server: {result['server']}\n")
                f.write(f"  Original ACAO: {result['original_acao']}\n")
                f.write(f"  Vulnerabilities:\n")
                
                for d in result['details']:
                    f.write(f"    - [{d['severity']}] {d['message']}\n")
                    f.write(f"      Origin: {d['origin']}\n")
                    f.write(f"      ACAO: {d['acao']}\n")
                    f.write(f"      Credentials: {d['allow_credentials']}\n\n")
        
        # JSON report
        with open(json_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"{Colors.GREEN}[✓] Report saved to: {report_file}{Colors.END}")
        print(f"{Colors.GREEN}[✓] JSON saved to: {json_file}{Colors.END}")

def main():
    parser = argparse.ArgumentParser(
        description='LINDSCORSCAN - Advanced CORS Misconfiguration Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
{Colors.CYAN}Examples:{Colors.END}
  python {sys.argv[0]} -u https://example.com
  python {sys.argv[0]} -l targets.txt -t 20 -o report.txt
  python {sys.argv[0]} -l targets.txt --timeout 10 --threads 50
        '''
    )
    
    parser.add_argument('-u', '--url', help='Single URL to scan')
    parser.add_argument('-l', '--list', help='File containing list of URLs to scan')
    parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
    parser.add_argument('--timeout', type=int, default=5, help='Request timeout in seconds (default: 5)')
    parser.add_argument('-o', '--output', help='Output file for report')
    parser.add_argument('--no-banner', action='store_true', help='Disable banner')
    
    args = parser.parse_args()
    
    if not args.url and not args.list:
        parser.print_help()
        print(f"\n{Colors.RED}[!] Please specify a target URL or list file{Colors.END}")
        sys.exit(1)
    
    scanner = CORSScanner(threads=args.threads, timeout=args.timeout, output_file=args.output)
    
    if not args.no_banner:
        scanner.print_banner()
    
    # Suppress SSL warnings
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    
    try:
        if args.url:
            scanner.scan_single(args.url)
        elif args.list:
            scanner.scan_multi(args.list)
        
        if scanner.results:
            scanner.generate_report()
            
            print(f"\n{Colors.RED}{'═'*80}{Colors.END}")
            print(f"{Colors.GREEN}[✓] Scan completed! Found {len(scanner.results)} vulnerable targets{Colors.END}")
            
            # Summary by severity
            critical = sum(1 for r in scanner.results if any(d['severity'] == 'CRITICAL' for d in r['details']))
            high = sum(1 for r in scanner.results if any(d['severity'] == 'HIGH' for d in r['details']))
            medium = sum(1 for r in scanner.results if any(d['severity'] == 'MEDIUM' for d in r['details']))
            
            print(f"{Colors.RED}    Critical: {critical}{Colors.END}")
            print(f"{Colors.YELLOW}    High: {high}{Colors.END}")
            print(f"{Colors.MAGENTA}    Medium: {medium}{Colors.END}")
            print(f"{Colors.RED}{'═'*80}{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}[*] No vulnerable targets found{Colors.END}")
            
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[!] Scan interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print(f"{Colors.RED}[!] Unexpected error: {e}{Colors.END}")
        sys.exit(1)

if __name__ == "__main__":
    main()
