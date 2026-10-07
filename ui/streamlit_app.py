import httpx
import streamlit as st

API_URL = "https://sentinel-olive-omega.vercel.app"

st.set_page_config(
    page_title="Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e6edf3;
    }
    [data-testid="stHeader"] {
        background-color: #0e1117;
    }
    [data-testid="stSidebar"] {
        background-color: #161b22;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #e6edf3 !important;
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        color: #58a6ff;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        color: #8b949e;
        margin-bottom: 1.5rem;
        font-size: 0.95rem;
    }
    .score-card {
        background: linear-gradient(135deg, #161b22 0%, #1c2128 100%);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
    }
    .score-value {
        font-size: 3.5rem;
        font-weight: 700;
        line-height: 1;
        margin-bottom: 0.3rem;
    }
    .score-label {
        color: #8b949e;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .score-good { color: #3fb950; }
    .score-mid  { color: #d29922; }
    .score-bad  { color: #f85149; }
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1rem 1.2rem;
        text-align: center;
    }
    .metric-num {
        font-size: 1.8rem;
        font-weight: 700;
        line-height: 1;
    }
    .metric-name {
        color: #8b949e;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.3rem;
    }
    .m-critical { color: #f85149; }
    .m-high     { color: #ff7b72; }
    .m-medium   { color: #d29922; }
    .m-low      { color: #58a6ff; }
    .finding-box {
        background-color: #161b22;
        border-left: 4px solid #30363d;
        border-radius: 6px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
    }
    .finding-pass    { border-left-color: #3fb950; }
    .finding-warning { border-left-color: #d29922; }
    .finding-fail    { border-left-color: #f85149; }
    .finding-title {
        font-weight: 600;
        color: #e6edf3;
        font-size: 0.95rem;
        margin-bottom: 0.3rem;
    }
    .finding-detail {
        color: #8b949e;
        font-size: 0.85rem;
    }
    .finding-rec {
        color: #58a6ff;
        font-size: 0.85rem;
        margin-top: 0.4rem;
    }
    .badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-right: 6px;
    }
    .b-critical { background: #f85149; color: #fff; }
    .b-high     { background: #ff7b72; color: #0e1117; }
    .b-medium   { background: #d29922; color: #0e1117; }
    .b-low      { background: #58a6ff; color: #0e1117; }
    .b-info     { background: #30363d; color: #8b949e; }
    .stButton > button {
        background-color: #238636;
        color: #fff;
        border: 1px solid #2ea043;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.5rem 1rem;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #2ea043;
        border-color: #3fb950;
    }
    .stTextInput > div > div > input {
        background-color: #0d1117;
        color: #e6edf3;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .stTextInput > div > div > input:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 2px rgba(88,166,255,0.2);
    }
    div[data-testid="stExpander"] {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 8px;
    }
    .ai-report {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 1.5rem;
        color: #e6edf3;
    }
    .endpoint-row {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 0.7rem 1rem;
        margin-bottom: 0.4rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        color: #79c0ff;
    }
    .status-ok  { color: #3fb950; font-weight: 700; }
    .status-red { color: #f85149; font-weight: 700; }
    .status-yel { color: #d29922; font-weight: 700; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🛡️ Sentinel</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Security scanner & AI analyst untuk website publik</div>',
    unsafe_allow_html=True,
)

col_url, col_deep, col_btn = st.columns([5, 1, 1])
with col_url:
    url = st.text_input(
        "URL target",
        placeholder="https://example.com",
        label_visibility="collapsed",
    )
with col_deep:
    deep = st.checkbox("Deep scan")
with col_btn:
    scan_clicked = st.button("Scan", use_container_width=True)

if scan_clicked and url:
    with st.spinner("Scanning target..."):
        try:
            r = httpx.post(
                f"{API}/scan",
                json={"url": url, "deep_scan": deep},
                timeout=180,
            )
            r.raise_for_status()
            data = r.json()
        except httpx.ConnectError:
            st.error("Tidak bisa konek ke API. Pastikan `uvicorn` jalan di port 8000.")
            st.stop()
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    score = data["score"]
    if score >= 80:
        score_class = "score-good"
        score_label = "SECURE"
    elif score >= 50:
        score_class = "score-mid"
        score_label = "NEEDS ATTENTION"
    else:
        score_class = "score-bad"
        score_label = "VULNERABLE"

    st.markdown("---")

    c1, c2 = st.columns([1, 2])

    with c1:
        st.markdown(
            f"""
            <div class="score-card">
                <div class="score-label">Security Score</div>
                <div class="score-value {score_class}">{score}</div>
                <div class="score-label">{score_label}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        s = data["summary"]
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-num m-critical">{s["critical"]}</div><div class="metric-name">Critical</div></div>',
                unsafe_allow_html=True,
            )
        with m2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-num m-high">{s["high"]}</div><div class="metric-name">High</div></div>',
                unsafe_allow_html=True,
            )
        with m3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-num m-medium">{s["medium"]}</div><div class="metric-name">Medium</div></div>',
                unsafe_allow_html=True,
            )
        with m4:
            st.markdown(
                f'<div class="metric-card"><div class="metric-num m-low">{s["low"]}</div><div class="metric-name">Low</div></div>',
                unsafe_allow_html=True,
            )

    st.markdown("")

    tab1, tab2 = st.tabs(["Findings", "Endpoints"])

    with tab1:
        findings = data["findings"]
        filter_col1, filter_col2 = st.columns([1, 3])
        with filter_col1:
            filter_status = st.selectbox(
                "Filter status",
                ["Semua", "Fail", "Warning", "Pass"],
                label_visibility="collapsed",
            )

        filtered = findings
        if filter_status == "Fail":
            filtered = [f for f in findings if f["status"] == "fail"]
        elif filter_status == "Warning":
            filtered = [f for f in findings if f["status"] == "warning"]
        elif filter_status == "Pass":
            filtered = [f for f in findings if f["status"] == "pass"]

        if not filtered:
            st.info("Tidak ada findings untuk filter ini.")
        else:
            for f in filtered:
                badge_class = f'b-{f["severity"]}'
                box_class = f'finding-{f["status"]}'
                rec_html = (
                    f'<div class="finding-rec">→ {f["recommendation"]}</div>'
                    if f.get("recommendation")
                    else ""
                )
                st.markdown(
                    f"""
                    <div class="finding-box {box_class}">
                        <div class="finding-title">
                            <span class="badge {badge_class}">{f["severity"].upper()}</span>
                            {f["title"]}
                        </div>
                        <div class="finding-detail">{f["detail"]}</div>
                        {rec_html}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    with tab2:
        endpoints = data.get("endpoints", [])
        if not endpoints:
            st.info("Tidak ada endpoint. Aktifkan **Deep scan** untuk meng-crawl struktur website.")
        else:
            st.caption(f"Total {len(endpoints)} endpoint ditemukan")
            for e in endpoints:
                if e["status"] < 300:
                    status_class = "status-ok"
                elif e["status"] < 400:
                    status_class = "status-yel"
                else:
                    status_class = "status-red"

                depth_indent = "&nbsp;&nbsp;" * e["depth"]
                st.markdown(
                    f"""
                    <div class="endpoint-row">
                        <span class="{status_class}">{e["status"]}</span>
                        &nbsp;&nbsp;{depth_indent}{e["url"]}
                        &nbsp;&nbsp;<span style="color:#8b949e;font-size:0.75rem;">[{e["content_type"]}]</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )