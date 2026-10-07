from collections import Counter

from app.models.scan import Finding

WEIGHTS = {"critical": 25, "high": 15, "medium": 8, "low": 3, "info": 0}


def calculate_score(findings: list[Finding]) -> int:
    score = 100
    for f in findings:
        if f.status in ("fail", "warning"):
            score -= WEIGHTS.get(f.severity, 0)
    return max(0, min(100, score))


def summarize(findings: list[Finding]) -> dict:
    counter = Counter()
    for f in findings:
        if f.status in ("fail", "warning"):
            counter[f.severity] += 1
    return {
        "critical": counter["critical"],
        "high": counter["high"],
        "medium": counter["medium"],
        "low": counter["low"],
        "total_issues": sum(counter.values()),
    }