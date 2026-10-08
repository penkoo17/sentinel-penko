"""Pembuat HTML untuk UI Sentinel.

Modul ini tidak meng-import streamlit supaya gampang dites. Semua teks yang
berasal dari hasil scan (judul, detail, URL, header target) di-escape, karena
isinya bisa dikontrol oleh website yang sedang di-scan.
"""
from __future__ import annotations

import math
from html import escape

from theme import BOARD_CSS, BOARD_JS, FONTS_URL

SEVERITIES = ["critical", "high", "medium", "low"]
LANES = SEVERITIES + ["info", "passed"]
STATUS_TAG = {"fail": "fail", "warning": "warn", "pass": "pass"}


def e(value) -> str:
    """Escape untuk HTML. '$' ikut di-escape agar tidak dibaca sebagai LaTeX oleh st.markdown."""
    return escape("" if value is None else str(value), quote=True).replace("$", "&#36;")


def _flat(markup: str) -> str:
    # st.markdown menganggap baris berindentasi / baris kosong sebagai code block.
    return "".join(line.strip() for line in markup.splitlines())


# ------------------------------------------------------------------ halaman
def brand() -> str:
    return _flat(
        """
        <div class="sn-top">
          <span class="sn-id"><span class="sn-mark"></span><span class="sn-brand">sentinel</span></span>
          <span class="sn-tag">Security scanner &amp; AI analyst untuk website publik</span>
        </div>
        """
    )

def brand_with_logo() -> str:
    """Header atas: logo + nama sentinel saja."""
    import base64
    from pathlib import Path

    logo_path = Path(__file__).parent / "assets" / "logo.png"
    if logo_path.exists():
        logo_b64 = base64.b64encode(logo_path.read_bytes()).decode()
        logo_html = (
            f'<img src="data:image/png;base64,{logo_b64}" '
            f'alt="Logo" style="width:24px;height:24px;border-radius:4px;display:block;object-fit:contain">'
        )
    else:
        logo_html = '<span class="sn-mark"></span>'

    return _flat(
        f"""
        <div class="sn-top">
          <span class="sn-id">
            {logo_html}
            <span class="sn-brand">sentinel</span>
          </span>
        </div>
        """
    )

def creator_bar() -> str:
    """Baris creator di atas form scan."""
    return _flat(
        """
        <div class="sn-creator-bar">
          <span class="sn-badge sn-badge-creator">CREATOR</span>
          <span class="sn-footer-name">PENKOO</span>
        </div>
        """
    )

def footer() -> str:
    return _flat(
        """
        <div class="sn-footer">
          <div class="sn-footer-left">
            <span class="sn-badge sn-badge-creator">CREATOR</span>
            <span class="sn-footer-name">PENKOO</span>
          </div>
        </div>
        """
    )

def hint() -> str:
    return (
        '<div class="sn-hint">Masukkan URL target lalu jalankan scan. '
        "Pakai hanya untuk website milik sendiri atau yang sudah ada izinnya.</div>"
    )


def notice(kind: str, text: str) -> str:
    return f'<div class="sn-note {"err" if kind == "err" else ""}">{e(text)}</div>'


def verdict(score: int) -> tuple[str, str]:
    if score >= 80:
        return "secure", "#4cc38a"
    if score >= 60:
        return "needs attention", "#e2c044"
    return "vulnerable", "#ff6369"


def summary(data: dict) -> str:
    score = max(0, min(100, int(data.get("score", 0))))
    label, color = verdict(score)
    s = data.get("summary") or {}
    issues = s.get("total_issues", sum(s.get(k, 0) for k in SEVERITIES))
    passed = sum(1 for f in data.get("findings", []) if f.get("status") == "pass")
    url = e(data.get("url", ""))
    return _flat(
        f"""
        <div class="sn-sum">
          <div class="sn-score"><span class="n" style="color:{color}">{score}</span><span class="of">/100</span></div>
          <div>
            <div class="sn-verdict" style="color:{color}">{label}</div>
            <div class="sn-meter" role="img" aria-label="Skor keamanan {score} dari 100"><i style="width:{score}%;background:{color}"></i></div>
            <div class="sn-target" title="{url}">{url}</div>
          </div>
          <dl class="sn-stats">
            <div><dt>temuan</dt><dd>{issues}</dd></div>
            <div><dt>lolos</dt><dd>{passed}</dd></div>
          </dl>
        </div>
        """
    )


# ------------------------------------------------------------------- papan
def group(findings: list[dict]) -> dict[str, list[dict]]:
    """Kelompokkan temuan ke lane. Status 'pass' masuk lane passed, sisanya sesuai severity."""
    lanes: dict[str, list[dict]] = {k: [] for k in LANES}
    for f in findings:
        if f.get("status") == "pass":
            lanes["passed"].append(f)
        else:
            sev = f.get("severity")
            lanes[sev if sev in LANES[:5] else "info"].append(f)
    for items in lanes.values():
        items.sort(key=lambda f: 0 if f.get("status") == "fail" else 1)
    return lanes


def _item(f: dict) -> str:
    tag = STATUS_TAG.get(f.get("status"), "info")
    detail = f'<p class="detail">{e(f.get("detail"))}</p>' if f.get("detail") else ""
    rec = f'<p class="fix"><i>saran</i><span>{e(f["recommendation"])}</span></p>' if f.get("recommendation") else ""
    fid = e(f.get("id"))
    return (
        f'<article class="item"><div class="top"><span class="st {tag}">{tag}</span>'
        f'<h3>{e(f.get("title"))}</h3><span class="fid" title="{fid}">{fid}</span></div>{detail}{rec}</article>'
    )


def _estimate(f: dict) -> int:
    """Perkiraan tinggi satu temuan (px), untuk menentukan tinggi iframe."""
    h = 29 + 22 * math.ceil(len(f.get("title") or "") / 34 or 1)
    if f.get("detail"):
        h += 8 + 20 * math.ceil(len(f["detail"]) / 50)
    if f.get("recommendation"):
        h += 8 + 20 * math.ceil(len(f["recommendation"]) / 46)
    return h


def board_doc(findings: list[dict]) -> tuple[str | None, int]:
    """Kembalikan (dokumen HTML, tinggi iframe). (None, 0) kalau tidak ada temuan."""
    lanes = group(findings)
    if not any(lanes.values()):
        return None, 0

    tabs, tracks, idx, tallest = [], [], 0, 0
    for key in LANES:
        items = lanes[key]
        if items:
            tabs.append(
                f'<button class="tab" role="tab" data-i="{idx}" aria-selected="false" style="--c:var(--{key})">'
                f'<i class="d"></i>{key} <b>{len(items)}</b></button>'
            )
            tracks.append(
                f'<section class="lane" aria-label="{key}" style="--c:var(--{key})">'
                f'<header>{key}<span>{len(items)}</span></header>'
                f'<div class="body">{"".join(_item(f) for f in items)}</div></section>'
            )
            tallest = max(tallest, 44 + sum(_estimate(f) for f in items))
            idx += 1
        elif key in SEVERITIES:  # severity yang tidak ditemukan tetap tampil sebagai "0" (redup)
            tabs.append(f'<span class="tab off" style="--c:var(--{key})"><i class="d"></i>{key} <b>0</b></span>')

    height = max(260, min(tallest, 540) + 46 + 12 + 14)
    doc = (
        '<!doctype html><html lang="id"><head><meta charset="utf-8">'
        '<meta name="color-scheme" content="dark">'
        f'<link rel="stylesheet" href="{FONTS_URL}"><style>{BOARD_CSS}</style></head><body>'
        '<div class="wrap"><div class="bar"><div class="tabs" role="tablist">' + "".join(tabs) + "</div>"
        '<div class="nav"><button id="prev" aria-label="Severity sebelumnya">&#8249;</button>'
        '<button id="next" aria-label="Severity berikutnya">&#8250;</button></div></div>'
        '<div class="track" id="track" tabindex="0" aria-label="Temuan per severity, geser ke samping">'
        + "".join(tracks)
        + f"</div></div><script>{BOARD_JS}</script></body></html>"
    )
    return doc, height


# --------------------------------------------------------------- endpoints
def endpoints_view(endpoints: list[dict]) -> str:
    rows = []
    for ep in endpoints:
        code = int(ep.get("status") or 0)
        cls = "ok" if code < 300 else "redir" if code < 400 else "bad"
        indent = min(int(ep.get("depth") or 0), 8) * 14
        rows.append(
            f'<div class="ep-row"><span class="code {cls}">{code}</span>'
            f'<span class="url" style="padding-left:{indent}px">{e(ep.get("url"))}</span>'
            f'<span class="ct">{e(ep.get("content_type"))}</span></div>'
        )
    return f'<div class="sn-cap">{len(rows)} endpoint ditemukan</div><div class="ep">{"".join(rows)}</div>'


# --------------------------------------------------------------- attack surface
def surface_view(surface: dict) -> str:
    """HTML view untuk attack surface."""
    if not surface:
        return ""

    parts = []

    ssl_info = surface.get("ssl") or {}
    if ssl_info and not ssl_info.get("error"):
        rows = [
            f'<div class="surface-k">{e("Issuer")}</div><div class="surface-v">{e(ssl_info.get("issuer", "-"))}</div>',
            f'<div class="surface-k">{e("Subject")}</div><div class="surface-v">{e(ssl_info.get("subject", "-"))}</div>',
            f'<div class="surface-k">{e("Expired")}</div><div class="surface-v">{e(ssl_info.get("not_after", "-"))}</div>',
            f'<div class="surface-k">{e("Sisa Hari")}</div><div class="surface-v">{e(ssl_info.get("days_left", "-"))}</div>',
            f'<div class="surface-k">{e("TLS")}</div><div class="surface-v">{e(ssl_info.get("tls_version", "-"))}</div>',
            f'<div class="surface-k">{e("Cipher")}</div><div class="surface-v">{e(ssl_info.get("cipher", "-"))}</div>',
            f'<div class="surface-k">{e("Jumlah SAN")}</div><div class="surface-v">{e(ssl_info.get("san_count", 0))}</div>',
        ]
        parts.append(f'<div class="surface-card"><h3>🔒 SSL/TLS</h3><div class="surface-grid">{"".join(rows)}</div></div>')

    dns = surface.get("dns") or {}
    if dns and not dns.get("error"):
        dns_rows = []
        for rtype in ("a", "aaaa", "mx", "txt", "ns"):
            values = dns.get(rtype) or []
            if values:
                joined = "<br>".join(e(v) for v in values)
                dns_rows.append(f'<div class="surface-k">{rtype.upper()}</div><div class="surface-v">{joined}</div>')
        if dns_rows:
            parts.append(f'<div class="surface-card"><h3>🌐 DNS Records</h3><div class="surface-grid">{"".join(dns_rows)}</div></div>')

    tech = surface.get("tech") or {}
    if tech and not tech.get("error"):
        techs = tech.get("technologies") or []
        server = tech.get("server", "-")
        powered = tech.get("powered_by", "") or "-"
        rows = [
            f'<div class="surface-k">{e("Server")}</div><div class="surface-v">{e(server)}</div>',
            f'<div class="surface-k">{e("Powered By")}</div><div class="surface-v">{e(powered)}</div>',
        ]
        if techs:
            tags = " ".join(f'<span class="tech-tag">{e(t)}</span>' for t in techs)
            rows.append(f'<div class="surface-k">{e("Terdeteksi")}</div><div class="surface-v">{tags}</div>')
        parts.append(f'<div class="surface-card"><h3>⚙️ Teknologi</h3><div class="surface-grid">{"".join(rows)}</div></div>')

    ports = surface.get("ports") or {}
    if ports and not ports.get("error"):
        open_ports = ports.get("open_ports") or []
        ip = ports.get("ip", "-")
        if open_ports:
            rows = "".join(
                f'<div class="port-row"><span class="port-num">{p["port"]}</span>'
                f'<span class="port-svc">{e(p["service"])}</span></div>'
                for p in open_ports
            )
        else:
            rows = '<div class="surface-v">Tidak ada port umum yang terbuka.</div>'
        parts.append(
            f'<div class="surface-card"><h3>🚪 Port Terbuka</h3>'
            f'<div class="surface-k">IP</div><div class="surface-v">{e(ip)}</div>'
            f'<div class="port-list">{rows}</div></div>'
        )

    if not parts:
        return '<div class="sn-note">Tidak ada info attack surface.</div>'

    return '<div class="surface-wrap">' + "".join(parts) + "</div>"