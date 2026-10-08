"""Deteksi teknologi dari header HTTP & isi HTML."""
import re

try:
    import httpx
    HAS_HTTPX = True
except ImportError:
    HAS_HTTPX = False


HEADER_SIGNATURES = [
    ("Cloudflare", r"cloudflare"),
    ("Nginx", r"nginx"),
    ("Apache", r"apache"),
    ("IIS", r"microsoft-iis"),
    ("LiteSpeed", r"litespeed"),
    ("Varnish", r"varnish"),
    ("WordPress", r"wordpress|wp-"),
    ("Drupal", r"drupal"),
    ("Joomla", r"joomla"),
    ("PHP", r"php"),
    ("ASP.NET", r"asp\.net"),
    ("Express", r"express"),
    ("Next.js", r"next\.js"),
    ("Node.js", r"node"),
    ("Python", r"python|uvicorn|gunicorn"),
    ("FastAPI", r"fastapi"),
]

HTML_SIGNATURES = [
    ("WordPress", r"wp-content|wp-includes"),
    ("Joomla", r"/components/com_"),
    ("Drupal", r"drupal\.js|sites/default"),
    ("Bootstrap", r"bootstrap(\.min)?\.css"),
    ("jQuery", r"jquery(\.min)?\.js"),
    ("React", r"react(\.production\.min)?\.js|__react"),
    ("Vue.js", r"vue(\.runtime)?(\.min)?\.js"),
    ("Angular", r"angular(\.min)?\.js"),
    ("Tailwind", r"tailwind"),
]


def detect_tech(url: str, timeout: float = 10.0) -> dict:
    """Return: server, powered_by, technologies[]."""
    if not HAS_HTTPX:
        return {"error": "httpx tidak terinstall"}

    if "://" not in url:
        url = "https://" + url

    try:
        r = httpx.get(url, timeout=timeout, follow_redirects=True, verify=False)
    except Exception as exc:
        return {"error": f"Fetch error: {exc}"}

    headers = {k.lower(): v for k, v in r.headers.items()}
    server = headers.get("server", "")
    powered_by = headers.get("x-powered-by", "")
    generator = headers.get("x-generator", "")

    techs = set()
    header_blob = " ".join(f"{k}:{v}" for k, v in headers.items()).lower()
    for name, pattern in HEADER_SIGNATURES:
        if re.search(pattern, header_blob):
            techs.add(name)

    try:
        html = r.text[:50000].lower()
        for name, pattern in HTML_SIGNATURES:
            if re.search(pattern, html):
                techs.add(name)
    except Exception:
        pass

    for c in r.cookies.jar:
        cname = c.name.lower()
        if "wordpress" in cname or cname.startswith("wp-"):
            techs.add("WordPress")
        if "joomla" in cname:
            techs.add("Joomla")
        if "drupal" in cname:
            techs.add("Drupal")
        if "laravel" in cname:
            techs.add("Laravel")

    return {
        "server": server or "Unknown",
        "powered_by": powered_by or "",
        "generator": generator or "",
        "technologies": sorted(techs),
        "status_code": r.status_code,
    }