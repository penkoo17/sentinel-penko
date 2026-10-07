import dns.resolver
from urllib.parse import urlparse

from app.models.scan import Finding


def scan_dns(url: str) -> list[Finding]:
    findings: list[Finding] = []
    host = urlparse(url).hostname
    if not host:
        return findings

    domain = ".".join(host.split(".")[-2:])

    try:
        txt_records = dns.resolver.resolve(domain, "TXT")
        has_spf = any("v=spf1" in str(r).lower() for r in txt_records)
    except Exception:
        has_spf = False

    if has_spf:
        findings.append(
            Finding(
                id="dns_spf",
                title="SPF Record",
                severity="info",
                status="pass",
                detail="SPF record ditemukan",
            )
        )
    else:
        findings.append(
            Finding(
                id="dns_spf_missing",
                title="SPF Record",
                severity="low",
                status="warning",
                detail="Tidak ada SPF record",
                recommendation="Tambahkan TXT record SPF untuk mencegah spoofing email",
            )
        )

    try:
        dmarc = dns.resolver.resolve(f"_dmarc.{domain}", "TXT")
        has_dmarc = any("v=dmarc1" in str(r).lower() for r in dmarc)
    except Exception:
        has_dmarc = False

    if has_dmarc:
        findings.append(
            Finding(
                id="dns_dmarc",
                title="DMARC Record",
                severity="info",
                status="pass",
                detail="DMARC record ditemukan",
            )
        )
    else:
        findings.append(
            Finding(
                id="dns_dmarc_missing",
                title="DMARC Record",
                severity="low",
                status="warning",
                detail="Tidak ada DMARC record",
                recommendation="Tambahkan DMARC policy untuk melindungi domain email",
            )
        )

    return findings