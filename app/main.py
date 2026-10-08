import asyncio

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

from app.analyzers import ai_analyst, scorer
from app.models.scan import ScanRequest, ScanResponse
from app.reports.generator import render_html
from app.scanners import (
    cookies,
    cors,
    crawler,
    dns_check,
    headers,
    js_parser,
    secrets,
    tls,
)

from app.models.scan import AttackSurfaceRequest
from app.analyzers.attack_surface import scan_attack_surface

app = FastAPI(title="Sentinel", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
async def home():
    return "<h1>Sentinel API</h1><p>POST /scan</p><p><a href='/docs'>/docs</a></p>"


@app.get("/health")
async def health():
    return {"status": "ok"}


async def _run_all(req: ScanRequest):
    url = str(req.url)
    findings = []

    # scanner async → jalankan paralel
    async_results = await asyncio.gather(
        headers.scan_headers(url),
        cookies.scan_cookies(url),
        cors.scan_cors(url),
        secrets.scan_secrets(url),
        return_exceptions=True,
    )
    for result in async_results:
        if isinstance(result, Exception):
            continue
        if result:
            findings.extend(result)

    # scanner sync → jalankan langsung
    try:
        findings.extend(dns_check.scan_dns(url))
    except Exception:
        pass

    try:
        findings.extend(tls.scan_tls(url))
    except Exception:
        pass

    # deep scan → crawler + attack surface
    endpoints = []
    attack_surface = None
    if req.deep_scan:
        try:
            endpoints = await crawler.crawl(url)
        except Exception:
            endpoints = []
        attack_surface = scan_attack_surface(url)

    score = scorer.calculate_score(findings)
    summary = scorer.summarize(findings)
    ai_report = await ai_analyst.generate_ai_report(url, score, findings)

    return ScanResponse(
        url=url,
        score=score,
        summary=summary,
        findings=findings,
        endpoints=endpoints,
        ai_report=ai_report,
        attack_surface=attack_surface,
    )

@app.post("/scan", response_model=ScanResponse)
async def scan(req: ScanRequest):
    try:
        return await _run_all(req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/scan/report", response_class=HTMLResponse)
async def scan_report(req: ScanRequest):
    report = await _run_all(req)
    return render_html(report)


@app.post("/scan/attack-surface")
def api_attack_surface(payload: AttackSurfaceRequest):
    """Scan attack surface: SSL, DNS, tech, ports."""
    return scan_attack_surface(payload.url)