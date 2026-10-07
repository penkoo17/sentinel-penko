from app.models.scan import Finding
from app.utils.http import make_client


async def scan_cors(url: str) -> list[Finding]:
    findings: list[Finding] = []
    async with make_client() as client:
        try:
            r = await client.get(url, headers={"Origin": "https://evil.example"})
        except Exception:
            return []

    acao = r.headers.get("access-control-allow-origin")
    acac = r.headers.get("access-control-allow-credentials")

    if not acao:
        return [
            Finding(
                id="cors_none",
                title="CORS",
                severity="info",
                status="pass",
                detail="Tidak ada header CORS yang di-set",
            )
        ]

    if acao == "*" and acac == "true":
        findings.append(
            Finding(
                id="cors_wildcard_creds",
                title="CORS Misconfiguration",
                severity="critical",
                status="fail",
                detail="Wildcard origin + credentials diizinkan",
                recommendation="Jangan kombinasikan wildcard dengan allow-credentials",
            )
        )
    elif acao == "*":
        findings.append(
            Finding(
                id="cors_wildcard",
                title="CORS Wildcard",
                severity="medium",
                status="warning",
                detail="Origin wildcard diizinkan untuk semua domain",
                recommendation="Batasi origin ke domain yang dipercaya",
            )
        )
    elif acao == "https://evil.example":
        findings.append(
            Finding(
                id="cors_reflect",
                title="CORS Reflects Origin",
                severity="high",
                status="fail",
                detail="Server memantulkan origin sembarang",
                recommendation="Whitelist origin yang valid saja",
            )
        )
    else:
        findings.append(
            Finding(
                id="cors_ok",
                title="CORS",
                severity="info",
                status="pass",
                detail=f"Origin dibatasi: {acao}",
            )
        )

    return findings