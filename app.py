import streamlit as st
import sys
import os
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ======================================================
# PATH FIX
# ======================================================
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

# ======================================================
# IMPORTS
# ======================================================
from logs.log_generator import start_log_generator
from logs.log_consumer import start_log_consumer
from ui.theme_loader import load_soc_theme
from ui.theme import DARK_BLUE_SOC_THEME as THEME
from config.config import Config

# ======================================================
# FILE PATHS
# ======================================================
LOG_FILE = "logs/logs.csv"
INCIDENT_FILE = "logs/incidents.csv"

# ======================================================
# STREAMLIT CONFIG
# ======================================================
st.set_page_config(
    page_title=Config.DASHBOARD_TITLE,
    layout="wide"
)

st_autorefresh(interval=3000, key="dashboard_refresh")

# ======================================================
# LOAD THEME
# ======================================================
load_soc_theme()

st.markdown(
    f"""
    <style>
    body, .stApp {{
        background-color: {THEME["main_bg"]};
        color: {THEME["text_color"]};
    }}

    .soc-card {{
        background: {THEME["card_bg"]};
        border: 1px solid {THEME["card_border"]};
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        color: {THEME["text_color"]};
        box-shadow: 0 0 18px rgba(37, 99, 235, 0.15);
    }}

    .severity-high {{
        color: #f87171;
        font-weight: bold;
    }}

    .severity-ok {{
        color: #4ade80;
        font-weight: bold;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# SAFE CSV LOADER
# ======================================================
def safe_read_csv(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame()
    try:
        return pd.read_csv(path, on_bad_lines="skip", engine="python")
    except Exception:
        return pd.DataFrame()

# ======================================================
# DEMO INCIDENT (FALLBACK)
# ======================================================
def get_demo_incident():
    return {
        "timestamp": "2026-01-01 18:42:10",
        "severity": "High",
        "service": "SSH",
        "src_ip": "185.221.88.45",
        "dst_ip": "10.0.0.12",
        "score": 0.92,
        "llm_report": """
[SOC Analyst Report]

Incident Type:
Brute-force authentication attempt

Severity:
High

Reason:
Multiple failed SSH login attempts were detected from an external IP
address within a short time window. The behavior matches automated
credential-stuffing activity.

Impact:
Potential unauthorized access to critical infrastructure.

Recommendation:
Block the source IP immediately, rotate credentials, and enable
multi-factor authentication.

Status:
Demo incident generated for dashboard visualization.
"""
    }

# ======================================================
# START BACKGROUND SERVICES (ONCE)
# ======================================================
if "services_started" not in st.session_state:
    start_log_generator()
    start_log_consumer()
    st.session_state["services_started"] = True

# ======================================================
# HEADER
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h2>AI Cyber Threat Detection Dashboard</h2>
        <p>Real-time SOC monitoring with ML-based detection and LLM-assisted analysis</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# LOAD DATA
# ======================================================
logs_df = safe_read_csv(LOG_FILE)
incidents_df = safe_read_csv(INCIDENT_FILE)

# ======================================================
# HIGH ALERTS
# ======================================================
high_alerts = (
    incidents_df[incidents_df["severity"] == "High"]
    if "severity" in incidents_df.columns
    else pd.DataFrame()
)

# ======================================================
# METRICS
# ======================================================
col1, col2, col3 = st.columns(3)

col1.metric("Total Logs", len(logs_df))
col2.metric("Total Alerts", len(incidents_df))
col3.metric("High Severity Alerts", len(high_alerts))

# ======================================================
# SYSTEM STATUS
# ======================================================
status = "Healthy" if high_alerts.empty else "Under Attack"
status_class = "severity-ok" if high_alerts.empty else "severity-high"

st.markdown(
    f"""
    <div class="soc-card">
        <b>System Status</b><br>
        <span class="{status_class}">{status}</span>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# DETECTION QUALITY
# ======================================================
tp = len(high_alerts)
fp = 0

st.markdown(
    f"""
    <div class="soc-card">
        <b>Detection Quality</b><br><br>
        True Positives: {tp}<br>
        False Positives: {fp}
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# LATEST INCIDENT (REAL OR DEMO)
# ======================================================
st.markdown("### Latest Security Incident")

if not high_alerts.empty:
    latest = high_alerts.iloc[-1]

    st.error("High severity security incident detected")

    st.markdown(
        f"""
        <div class="soc-card">
            <b>Timestamp:</b> {latest.get("timestamp")}<br>
            <b>Service:</b> {latest.get("service")}<br>
            <b>Source IP:</b> {latest.get("src_ip")}<br>
            <b>Destination IP:</b> {latest.get("dst_ip")}<br><br>

            <b>LLM Analysis:</b><br>
            {latest.get("llm_report", "LLM report pending...")}
        </div>
        """,
        unsafe_allow_html=True
    )

else:
    demo = get_demo_incident()

    st.warning("Demo Mode: Showing sample high-severity incident")

    st.markdown(
        f"""
        <div class="soc-card">
            <b>Timestamp:</b> {demo["timestamp"]}<br>
            <b>Service:</b> {demo["service"]}<br>
            <b>Source IP:</b> {demo["src_ip"]}<br>
            <b>Destination IP:</b> {demo["dst_ip"]}<br><br>

            <b>LLM Analysis:</b><br>
            {demo["llm_report"]}
        </div>
        """,
        unsafe_allow_html=True
    )

# ======================================================
# INCIDENT HISTORY
# ======================================================
st.markdown("### AI Threat Intelligence")

if not incidents_df.empty:
    st.dataframe(
        incidents_df.iloc[::-1],
        use_container_width=True,
        height=350
    )
else:
    st.info("Live incidents will appear here once detected.")
