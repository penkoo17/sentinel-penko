from app.models.scan import Finding
from app.utils.http import make_client

SECURITY_HEADERS = {
    "strict-transport-security": {
        "title": "HSTS",
        "severity": "high",
        "rec": "Tambahkan Strict-Transport-Security: max-age=31536000; includeSubDomains",
    },
    "content-security-policy": {
        "title": "CSP",
        "severity": "high",
        "rec": "Implementasikan Content-Security-Policy untuk mitigasi XSS",
    },
    "x-frame-options": {
        "title": "X-Frame-Options",
        "severity": "medium",
        "rec": "Set X-Frame-Options: DENY atau SAMEORIGIN",
    },
    "x-content-type-options": {
        "title": "X-Content-Type-Options",
        "severity": "medium",
        "rec": "Set X-Content-Type-Options: nosniff",
    },
    "referrer-policy": {
        "title": "Referrer-Policy",
        "severity": "low",
        "rec": "Set Referrer-Policy: strict-origin-when-cross-origin",
    },
    "permissions-policy": {
        "title": "Permissions-Policy",
        "severity": "low",
        "rec": "Batasi fitur browser yang tidak dipakai",
    },
}


async def scan_headers(url: str) -> list[Finding]:
    findings: list[Finding] = []
    async with make_client() as client:
        try:
            r = await client.get(url)
        except Exception as e:
            return [
                Finding(
                    id="conn_error",
                    title="Connection Failed",
                    severity="critical",
                    status="fail",
                    detail=str(e),
                    recommendation="Pastikan URL dapat diakses publik",
                )
            ]

    headers = {k.lower(): v for k, v in r.headers.items()}

    for key, meta in SECURITY_HEADERS.items():
        if key in headers:
            findings.append(
                Finding(
                    id=key,
                    title=meta["title"],
                    severity=meta["severity"],
                    status="pass",
                    detail=f"Header terpasang: {headers[key][:120]}",
                )
            )
        else:
            findings.append(
                Finding(
                    id=key,
                    title=meta["title"],
                    severity=meta["severity"],
                    status="fail",
                    detail="Header tidak ditemukan",
                    recommendation=meta["rec"],
                )
            )

    for h in ["server", "x-powered-by", "x-aspnet-version"]:
        if h in headers:
            findings.append(
                Finding(
                    id=f"info_{h}",
                    title=f"Information Disclosure: {h}",
                    severity="low",
                    status="warning",
                    detail=f"{h}: {headers[h]}",
                    recommendation=f"Sembunyikan atau samarkan header {h}",
                )
            )

    return findings