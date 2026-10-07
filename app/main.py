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
    findings.extend(await headers.scan_headers(url))
    findings.extend(await cookies.scan_cookies(url))
    findings.extend(tls.scan_tls(url))
    findings.extend(await cors.scan_cors(url))
    findings.extend(dns_check.scan_dns(url))
    findings.extend(await secrets.scan_secrets(url))
    findings.extend(await js_parser.scan_js_endpoints(url))

    endpoints = []
    if req.deep_scan:
        endpoints = await crawler.crawl(url)

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