import ssl
import socket
from urllib.parse import urlparse
from datetime import datetime, timezone

from app.models.scan import Finding


def scan_tls(url: str) -> list[Finding]:
    findings: list[Finding] = []
    parsed = urlparse(url)

    if parsed.scheme != "https":
        findings.append(
            Finding(
                id="https_missing",
                title="HTTPS",
                severity="critical",
                status="fail",
                detail="Website tidak menggunakan HTTPS",
                recommendation="Pasang sertifikat TLS dan redirect HTTP ke HTTPS",
            )
        )
        return findings

    host = parsed.hostname
    port = parsed.port or 443

    try:
        ctx = ssl.create_default_context()
        with socket.create_connection((host, port), timeout=10) as sock:
            with ctx.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                version = ssock.version()
    except Exception as e:
        findings.append(
            Finding(
                id="tls_error",
                title="TLS Handshake",
                severity="high",
                status="fail",
                detail=str(e),
                recommendation="Periksa konfigurasi TLS server",
            )
        )
        return findings

    findings.append(
        Finding(
            id="tls_version",
            title="TLS Version",
            severity="info",
            status="pass" if version in ("TLSv1.2", "TLSv1.3") else "warning",
            detail=f"Menggunakan {version}",
            recommendation=None
            if version in ("TLSv1.2", "TLSv1.3")
            else "Upgrade ke TLS 1.2 atau 1.3",
        )
    )

    not_after = cert.get("notAfter")
    if not_after:
        exp = datetime.strptime(not_after, "%b %d %H:%M:%S %Y %Z").replace(
            tzinfo=timezone.utc
        )
        days_left = (exp - datetime.now(timezone.utc)).days
        if days_left < 0:
            findings.append(
                Finding(
                    id="cert_expired",
                    title="Certificate Expired",
                    severity="critical",
                    status="fail",
                    detail=f"Sertifikat kadaluarsa {abs(days_left)} hari lalu",
                    recommendation="Perbarui sertifikat TLS",
                )
            )
        elif days_left < 14:
            findings.append(
                Finding(
                    id="cert_expiring",
                    title="Certificate Expiring Soon",
                    severity="high",
                    status="warning",
                    detail=f"Sertifikat kadaluarsa dalam {days_left} hari",
                    recommendation="Perbarui sertifikat TLS",
                )
            )
        else:
            findings.append(
                Finding(
                    id="cert_valid",
                    title="Certificate Validity",
                    severity="info",
                    status="pass",
                    detail=f"Berlaku {days_left} hari lagi",
                )
            )

    return findings