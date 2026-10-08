import os

import httpx
import streamlit as st
from pathlib import Path

from theme import APP_CSS
from views import board_doc, brand_with_logo, creator_bar, endpoints_view, hint, notice, summary, surface_view

import os

API = os.getenv("SENTINEL_API_URL", "https://sentinel-olive-omega.vercel.app")

st.set_page_config(
    page_title="Sentinel",
    page_icon=str(Path(__file__).parent / "assets" / "logo.png"),
    layout="wide",
    initial_sidebar_state="collapsed",
)
st.markdown(f"<style>{APP_CSS}</style>", unsafe_allow_html=True)


def embed(doc: str, height: int) -> None:
    """st.iframe di Streamlit baru, components.html di versi lama."""
    if hasattr(st, "iframe"):
        st.iframe(doc, height=height)
    else:
        import streamlit.components.v1 as components

        components.html(doc, height=height)


def run_scan(url: str, deep: bool):
    try:
        r = httpx.post(f"{API}/scan", json={"url": url, "deep_scan": deep}, timeout=180)
        r.raise_for_status()
        return r.json(), None
    except httpx.ConnectError:
        return None, "Tidak bisa konek ke API. Pastikan uvicorn jalan di port 8000."
    except Exception as exc:
        return None, f"Error: {exc}"


st.markdown(brand_with_logo(), unsafe_allow_html=True)
st.markdown(creator_bar(), unsafe_allow_html=True)

with st.form("scan", border=False):
    c_url, c_deep, c_go = st.columns([6, 1.3, 1], vertical_alignment="center")
    url = c_url.text_input("URL target", placeholder="https://example.com", label_visibility="collapsed")
    deep = c_deep.checkbox("Deep scan")
    go = c_go.form_submit_button("Scan")

if go:
    target = url.strip()
    if not target:
        st.markdown(notice("err", "Masukkan URL target dulu."), unsafe_allow_html=True)
        st.stop()
    if "://" not in target:
        target = "https://" + target
    with st.spinner("scanning target…"):
        data, err = run_scan(target, deep)
    if err:
        st.markdown(notice("err", err), unsafe_allow_html=True)
        st.stop()
    st.session_state["scan_result"] = data

data = st.session_state.get("scan_result")
if data is None:
    st.markdown(hint(), unsafe_allow_html=True)
    st.stop()

st.markdown(summary(data), unsafe_allow_html=True)

endpoints = data.get("endpoints") or []
attack_surface = data.get("attack_surface")

tab_labels = ["findings", f"endpoints ({len(endpoints)})"]
if attack_surface:
    tab_labels.append("attack surface")

tab_objs = st.tabs(tab_labels)
tab_findings = tab_objs[0]
tab_endpoints = tab_objs[1]
tab_surface = tab_objs[2] if len(tab_objs) > 2 else None

with tab_findings:
    doc, height = board_doc(data.get("findings") or [])
    if doc:
        embed(doc, height)
    else:
        st.markdown(notice("info", "Tidak ada temuan untuk target ini."), unsafe_allow_html=True)

with tab_endpoints:
    if endpoints:
        st.markdown(endpoints_view(endpoints), unsafe_allow_html=True)
    else:
        st.markdown(
            notice("info", "Belum ada endpoint. Aktifkan Deep scan untuk meng-crawl struktur website."),
            unsafe_allow_html=True,
        )

if tab_surface is not None:
    with tab_surface:
        st.markdown(surface_view(attack_surface), unsafe_allow_html=True)
       