import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from services import get_service_info

class PortScanner:
    def __init__(self, target, ports, timeout=2.0, threads=10, grab_banners=False):
        self.target = target
        self.ports = self._parse_ports(ports)
        self.timeout = timeout
        self.threads = threads
        self.grab_banners = grab_banners
        self.results = []
        self.lock = threading.Lock()

    def _parse_ports(self, ports):
        if isinstance(ports, list):
            return ports
        if '-' in str(ports):
            start, end = map(int, ports.split('-'))
            return list(range(start, end + 1))
        return [int(ports)]

    def _grab_banner(self, s):
        try:
            s.send(b'HEAD / HTTP/1.0\r\n\r\n')
            return s.recv(1024).decode('utf-8', errors='ignore').strip()
        except:
            return None

    def scan_port(self, port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(self.timeout)
                result = s.connect_ex((self.target, port))
                if result == 0:
                    service = get_service_info(port)
                    banner = self._grab_banner(s) if self.grab_banners else None
                    
                    with self.lock:
                        self.results.append({
                            "port": port,
                            "status": "open",
                            "service": service.get("name", "unknown"),
                            "implication": service.get("implication", "N/A"),
                            "banner": banner
                        })
        except Exception:
            pass

    def run(self):
        try:
            socket.gethostbyname(self.target)
        except socket.gaierror:
            print(f"[!] Error: Could not resolve host {self.target}")
            return []

        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            executor.map(self.scan_port, self.ports)
        
        return sorted(self.results, key=lambda x: x['port'])
