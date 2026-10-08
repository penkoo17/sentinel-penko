"""Ambil info sertifikat SSL/TLS dari target."""
import socket
import ssl
from datetime import datetime, timezone
from urllib.parse import urlparse


def _get_cert_binary(host: str, port: int, timeout: float) -> bytes | None:
    """Ambil cert dalam bentuk binary DER, decode manual."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    with socket.create_connection((host, port), timeout=timeout) as sock:
        with ctx.wrap_socket(sock, server_hostname=host) as ssock:
            return ssock.getpeercert(binary_form=True)


def get_ssl_info(url: str, timeout: float = 5.0) -> dict:
    """Return info sertifikat SSL target."""
    parsed = urlparse(url if "://" in url else f"https://{url}")
    host = parsed.hostname
    port = parsed.port or 443

    if not host:
        return {"error": "Host tidak valid"}

    try:
        # pakai CERT_OPTIONAL biar cert bisa di-parse
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_OPTIONAL

        with socket.create_connection((host, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                cipher = ssock.cipher()
                version = ssock.version()

        if not cert:
            # fallback: ambil DER lalu coba parse pakai ssl._ssl._test_decode_cert
            # kalau masih gagal, return info minimal
            return {
                "issuer": "Tidak tersedia",
                "subject": host,
                "not_before": "",
                "not_after": "",
                "days_left": None,
                "san_count": 0,
                "sans": [],
                "tls_version": version,
                "cipher": cipher[0] if cipher else "",
            }

        issuer = dict(x[0] for x in cert.get("issuer", []))
        subject = dict(x[0] for x in cert.get("subject", []))
        sans = [v for k, v in cert.get("subjectAltName", []) if k == "DNS"]
        not_before = cert.get("notBefore", "")
        not_after = cert.get("notAfter", "")

        days_left = None
        try:
            expire = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
            days_left = (expire - datetime.now(timezone.utc)).days
        except Exception:
            pass

        return {
            "issuer": issuer.get("organizationName") or issuer.get("commonName", ""),
            "subject": subject.get("commonName", ""),
            "not_before": not_before,
            "not_after": not_after,
            "days_left": days_left,
            "san_count": len(sans),
            "sans": sans[:10],
            "tls_version": version,
            "cipher": cipher[0] if cipher else "",
        }
    except Exception as exc:
        return {"error": f"SSL error: {exc}"}