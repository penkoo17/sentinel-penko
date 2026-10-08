"""Attack Surface Analyzer — kumpulkan info dari target."""
from .ssl_info import get_ssl_info
from .dns_info import get_dns_info
from .tech_detect import detect_tech
from .ports import scan_ports


def scan_attack_surface(url: str) -> dict:
    """Jalankan semua analyzer attack surface."""
    return {
        "url": url,
        "ssl": get_ssl_info(url),
        "dns": get_dns_info(url),
        "tech": detect_tech(url),
        "ports": scan_ports(url),
    }