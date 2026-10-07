import asyncio
from collections import deque
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup

from app.config import MAX_CRAWL_DEPTH, MAX_CRAWL_PAGES, REQUEST_DELAY
from app.models.scan import Endpoint
from app.utils.http import make_client


async def crawl(base_url: str) -> list[Endpoint]:
    visited: set[str] = set()
    queue: deque = deque([(base_url, 0)])
    results: list[Endpoint] = []
    base_domain = urlparse(base_url).netloc

    async with make_client() as client:
        while queue and len(visited) < MAX_CRAWL_PAGES:
            url, depth = queue.popleft()
            if url in visited or depth > MAX_CRAWL_DEPTH:
                continue
            visited.add(url)

            try:
                r = await client.get(url)
                ct = r.headers.get("content-type", "").split(";")[0]
                results.append(
                    Endpoint(url=url, status=r.status_code, content_type=ct, depth=depth)
                )

                if "text/html" in ct:
                    soup = BeautifulSoup(r.text, "lxml")
                    for a in soup.find_all("a", href=True):
                        link = urljoin(url, a["href"]).split("#")[0]
                        if urlparse(link).netloc == base_domain and link not in visited:
                            queue.append((link, depth + 1))
            except Exception:
                continue

            await asyncio.sleep(REQUEST_DELAY)

    return results