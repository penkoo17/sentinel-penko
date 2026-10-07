import httpx
from app.config import SCAN_TIMEOUT

USER_AGENT = "Sentinel-Scanner/0.1"


def make_client(**kwargs) -> httpx.AsyncClient:
    return httpx.AsyncClient(
        timeout=SCAN_TIMEOUT,
        follow_redirects=True,
        headers={"User-Agent": USER_AGENT},
        verify=True,
        **kwargs,
    )