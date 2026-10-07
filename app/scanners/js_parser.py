import re
from urllib.parse import urlparse

from app.models.scan import Finding
from app.utils.http import make_client

ENDPOINT_RE = re.compile(
    r"""["'`](/(?:api|v\d+|graphql|rest|auth|user|admin)[\w\-./?=&%]*)["'`]"""
)
SCRIPT_SRC_RE = re.compile(r"""<script[^>]+src=["']([^"']+)["']""")


async def scan_js_endpoints(url: str) -> list[Finding]:
    findings: list[Finding] = []
    parsed = urlparse(url)
    base = f"{parsed.scheme}://{parsed.netloc}"

    async with make_client() as client:
        try:
            r = await client.get(url)
        except Exception:
            return findings

        scripts = SCRIPT_SRC_RE.findall(r.text)
        endpoints: set[str] = set()

        for src in scripts[:10]:
            if src.startswith("//"):
                src = f"{parsed.scheme}:{src}"
            elif src.startswith("/"):
                src = base + src
            elif not src.startswith("http"):
                src = base + "/" + src

            try:
                js = await client.get(src)
                endpoints.update(ENDPOINT_RE.findall(js.text))
            except Exception:
                continue

    if endpoints:
        findings.append(
            Finding(
                id="js_endpoints",
                title="Endpoints Found in JavaScript",
                severity="low",
                status="warning",
                detail=f"{len(endpoints)} endpoint terdeteksi: "
                + ", ".join(sorted(endpoints)[:10]),
                recommendation="Pastikan endpoint tidak mengekspos data sensitif",
            )
        )
    return findings