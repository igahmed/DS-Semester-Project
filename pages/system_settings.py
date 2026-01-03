import sys
import os
import streamlit as st

# ======================================================
# PATH FIX
# ======================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from config.config import Config
from ui.theme_loader import load_soc_theme

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(page_title="System Settings", layout="wide")
load_soc_theme()

# ======================================================
# HEADER
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h2>System Settings</h2>
        <p>Configuration and status overview</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# SYSTEM STATUS
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h3>System Status</h3>
        <b>Log Simulation:</b> Enabled<br>
        <b>ML Engine:</b> Active<br>
        <b>LLM Engine:</b> Active
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# CONFIGURATION DETAILS
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h3>Configuration</h3>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div class="soc-card">
            <b>Dashboard Title</b><br>
            {Config.DASHBOARD_TITLE}<br><br>

            <b>Log Simulation Rate</b><br>
            {Config.LOG_SIMULATION_RATE} logs/sec<br><br>

            <b>Simulation Enabled</b><br>
            {Config.SIMULATION_ENABLED}
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="soc-card">
            <b>ML Model Path</b><br>
            {Config.ML_MODEL_PATH}<br><br>

            <b>LLM Endpoint</b><br>
            {Config.LLM_ENDPOINT}<br><br>

            <b>Threat History File</b><br>
            {Config.THREAT_HISTORY_FILE}
        </div>
        """,
        unsafe_allow_html=True
    )


st.info(
    "These settings are currently read-only. "
    "Future versions may allow live configuration updates and service restarts."
)
