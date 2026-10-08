"""Ambil DNS records target."""
from urllib.parse import urlparse

try:
    import dns.resolver
    HAS_DNS = True
except ImportError:
    HAS_DNS = False


def get_dns_info(url: str) -> dict:
    """Return DNS records: A, AAAA, MX, TXT, NS."""
    if not HAS_DNS:
        return {"error": "dnspython tidak terinstall"}

    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.hostname
    if not host:
        return {"error": "Host tidak valid"}

    result: dict[str, list] = {}

    for rtype in ("A", "AAAA", "MX", "TXT", "NS"):
        try:
            answers = dns.resolver.resolve(host, rtype, lifetime=5)
            values = []
            for r in answers:
                if rtype == "MX":
                    values.append(f"{r.preference} {r.exchange}")
                else:
                    values.append(str(r).strip('"'))
            result[rtype.lower()] = values[:10]
        except Exception:
            result[rtype.lower()] = []

    return result