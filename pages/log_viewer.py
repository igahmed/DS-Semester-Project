import sys
import os
import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# ======================================================
# PATH FIX
# ======================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ui.theme_loader import load_soc_theme
from ui.theme import DARK_BLUE_SOC_THEME as THEME

LOG_FILE = "logs/logs.csv"

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Live Log Viewer",
    layout="wide"
)

# ======================================================
# AUTO REFRESH
# ======================================================
st_autorefresh(interval=4000, key="log_refresh")

# ======================================================
# LOAD THEME (SAME AS app.py)
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

    table {{
        width: 100%;
        border-collapse: collapse;
    }}

    th {{
        background-color: {THEME["table_header_bg"]};
        color: {THEME["table_header_color"]};
        padding: 8px;
        text-align: left;
        border-bottom: 1px solid {THEME["card_border"]};
    }}

    td {{
        background-color: {THEME["table_row_bg"]};
        color: {THEME["table_row_color"]};
        padding: 6px;
        border-bottom: 1px solid {THEME["card_border"]};
    }}

    tr:hover td {{
        background-color: #0f1f3a;
    }}

    ::-webkit-scrollbar {{
        width: 8px;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #2563eb;
        border-radius: 10px;
    }}
    ::-webkit-scrollbar-track {{
        background: #020617;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# LOAD LOGS SAFELY
# ======================================================
if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
    st.warning("No logs available yet.")
    st.stop()

try:
    df = pd.read_csv(LOG_FILE, on_bad_lines="skip", engine="python")
except Exception as e:
    st.error(f"Error reading logs: {e}")
    st.stop()

if df.empty:
    st.info("Waiting for incoming logs.")
    st.stop()

# Show latest logs first
df = df.iloc[::-1]

# ======================================================
# HEADER
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h2>Live Security Logs</h2>
        <p>Real-time log stream generated and monitored by the SOC system</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# LOG TABLE (SOC STYLE)
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h3>Incoming Log Stream</h3>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="soc-card" style="max-height: 520px; overflow-y: auto;">
        {df.to_html(index=False, escape=False)}
    </div>
    """,
    unsafe_allow_html=True
)
