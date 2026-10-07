from app.models.scan import Finding


async def generate_ai_report(url: str, score: int, findings: list[Finding]) -> str:
    return None