from app.models.scan import Finding
from app.utils.http import make_client


async def scan_cookies(url: str) -> list[Finding]:
    findings: list[Finding] = []
    async with make_client() as client:
        try:
            r = await client.get(url)
        except Exception:
            return []

    raw_headers = r.headers.get_list("set-cookie")
    if not raw_headers:
        return [
            Finding(
                id="cookies_none",
                title="Cookies",
                severity="info",
                status="pass",
                detail="Tidak ada cookie yang di-set",
            )
        ]

    for raw in raw_headers:
        parts = raw.split(";")
        name = parts[0].split("=")[0].strip()
        flags = [p.strip().lower() for p in parts[1:]]

        issues = []
        if not any(f.startswith("secure") for f in flags):
            issues.append("Secure")
        if not any(f.startswith("httponly") for f in flags):
            issues.append("HttpOnly")
        if not any(f.startswith("samesite") for f in flags):
            issues.append("SameSite")

        if issues:
            findings.append(
                Finding(
                    id=f"cookie_{name}",
                    title=f"Cookie: {name}",
                    severity="medium",
                    status="warning",
                    detail=f"Flag hilang: {', '.join(issues)}",
                    recommendation=f"Tambahkan flag: {', '.join(issues)}",
                )
            )
        else:
            findings.append(
                Finding(
                    id=f"cookie_{name}",
                    title=f"Cookie: {name}",
                    severity="info",
                    status="pass",
                    detail="Konfigurasi cookie aman",
                )
            )

    return findings