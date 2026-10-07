import re

from app.models.scan import Finding
from app.utils.http import make_client

PATTERNS = {
    "Google API Key": r"AIza[0-9A-Za-z\-_]{35}",
    "AWS Access Key": r"AKIA[0-9A-Z]{16}",
    "Stripe Key": r"sk_live_[0-9a-zA-Z]{24,}",
    "GitHub Token": r"ghp_[0-9A-Za-z]{36}",
    "Slack Token": r"xox[baprs]-[0-9A-Za-z\-]{10,}",
    "Private Key": r"-----BEGIN (RSA|EC|DSA|OPENSSH) PRIVATE KEY-----",
    "JWT": r"eyJ[A-Za-z0-9_\-]+\.eyJ[A-Za-z0-9_\-]+\.[A-Za-z0-9_\-]+",
}


async def scan_secrets(url: str) -> list[Finding]:
    findings: list[Finding] = []
    async with make_client() as client:
        try:
            r = await client.get(url)
        except Exception:
            return findings

    body = r.text
    for name, pattern in PATTERNS.items():
        matches = re.findall(pattern, body)
        if matches:
            findings.append(
                Finding(
                    id=f"secret_{name.lower().replace(' ', '_')}",
                    title=f"Exposed Secret: {name}",
                    severity="critical",
                    status="fail",
                    detail=f"{len(matches)} kemungkinan {name} ditemukan di HTML",
                    recommendation="Rotasi kredensial dan jangan expose di client-side",
                )
            )

    return findings