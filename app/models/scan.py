from pydantic import BaseModel, HttpUrl
from typing import Optional, Literal

Severity = Literal["critical", "high", "medium", "low", "info"]
Status = Literal["pass", "warning", "fail"]


class ScanRequest(BaseModel):
    url: HttpUrl
    deep_scan: bool = False


class Finding(BaseModel):
    id: str
    title: str
    severity: Severity
    status: Status
    detail: str
    recommendation: Optional[str] = None


class Endpoint(BaseModel):
    url: str
    status: int
    content_type: str
    depth: int


class ScanResponse(BaseModel):
    url: str
    score: int
    summary: dict
    findings: list[Finding]
    endpoints: list[Endpoint] = []
    ai_report: Optional[str] = None