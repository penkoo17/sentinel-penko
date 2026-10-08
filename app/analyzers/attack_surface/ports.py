"""Scan port umum. Pakai socket standard lib."""
import socket
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed


COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 143, 443, 445,
    3306, 3389, 5432, 5900, 6379, 8080, 8443, 9200, 27017,
]

PORT_LABELS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL", 5900: "VNC",
    6379: "Redis", 8080: "HTTP-Alt", 8443: "HTTPS-Alt",
    9200: "Elasticsearch", 27017: "MongoDB",
}


def _check_port(host: str, port: int, timeout: float = 1.0):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            return port if s.connect_ex((host, port)) == 0 else None
    except Exception:
        return None


def scan_ports(url: str, timeout: float = 1.0, max_workers: int = 20) -> dict:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.hostname
    if not host:
        return {"error": "Host tidak valid"}

    try:
        ip = socket.gethostbyname(host)
    except Exception as exc:
        return {"error": f"DNS resolve gagal: {exc}"}

    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(_check_port, ip, p, timeout): p for p in COMMON_PORTS}
        for fut in as_completed(futures):
            result = fut.result()
            if result is not None:
                open_ports.append(result)

    open_ports.sort()
    return {
        "ip": ip,
        "open_ports": [{"port": p, "service": PORT_LABELS.get(p, "?")} for p in open_ports],
        "total_scanned": len(COMMON_PORTS),
    }