from app.analyzers.scorer import calculate_score, summarize
from app.models.scan import Finding


def test_score_perfect():
    assert calculate_score([]) == 100


def test_score_critical():
    f = [Finding(id="x", title="x", severity="critical", status="fail", detail="d")]
    assert calculate_score(f) == 75


def test_score_floor():
    f = [
        Finding(id=f"x{i}", title="x", severity="critical", status="fail", detail="d")
        for i in range(10)
    ]
    assert calculate_score(f) == 0


def test_summary():
    f = [
        Finding(id="a", title="a", severity="high", status="fail", detail="d"),
        Finding(id="b", title="b", severity="high", status="pass", detail="d"),
        Finding(id="c", title="c", severity="low", status="warning", detail="d"),
    ]
    s = summarize(f)
    assert s["high"] == 1
    assert s["low"] == 1
    assert s["total_issues"] == 2