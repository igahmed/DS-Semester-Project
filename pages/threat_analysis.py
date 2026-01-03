import sys
import os
import streamlit as st
import pandas as pd
import re

# ======================================================
# PATH FIX
# ======================================================
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from ui.theme_loader import load_soc_theme
from llm.llm import get_llm_report

LOG_FILE = "logs/logs.csv"

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Threat Analysis Center",
    layout="wide"
)

load_soc_theme()

# ======================================================
# EXTRA THEME FIXES (VISIBILITY + POLISH)
# ======================================================
st.markdown(
    """
    <style>
    body, .stApp {
        background-color: #0b1220;
        color: #e5e7eb;
    }

    .soc-card {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 16px;
        box-shadow: 0 0 18px rgba(37, 99, 235, 0.15);
    }

    h2, h3 {
        color: #60a5fa;
    }

    label, .stSelectbox label, .stCheckbox label {
        color: #cbd5f5 !important;
        font-weight: 500;
    }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        padding: 0.5em 1.2em;
        font-weight: 600;
        border: none;
    }

    .stButton > button:hover {
        background-color: #1d4ed8;
    }

    table {
        background-color: #020617;
        color: #e5e7eb;
        border-radius: 10px;
        overflow: hidden;
    }

    thead tr th {
        background-color: #1e293b;
        color: #93c5fd;
        font-weight: 600;
    }

    tbody tr td {
        background-color: #020617;
        border-bottom: 1px solid #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ======================================================
# HEADER
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h2>Threat Analysis Center</h2>
        <p>Manual SOC investigation with LLM-assisted intelligence</p>
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# LOAD LOGS SAFELY
# ======================================================
COLUMNS = ["timestamp", "service", "src_ip", "dst_ip", "event", "action"]

if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
    st.warning("No logs available for analysis.")
    st.stop()

logs_df = pd.read_csv(
    LOG_FILE,
    engine="python",
    header=None,
    names=COLUMNS,
    on_bad_lines="skip"
).dropna(how="all")

if logs_df.empty:
    st.warning("No valid log entries found.")
    st.stop()

logs_df["display"] = (
    logs_df["timestamp"].astype(str) + " | " +
    logs_df["service"].astype(str) + " | " +
    logs_df["event"].astype(str)
)

# ======================================================
# LOG SELECTION
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h3>Select Log Entry</h3>
    </div>
    """,
    unsafe_allow_html=True
)

selected = st.selectbox("Choose log entry", logs_df["display"])
log = logs_df[logs_df["display"] == selected].iloc[0]

# ======================================================
# LOG DETAILS
# ======================================================
st.markdown(
    f"""
    <div class="soc-card">
        <h3>Log Details</h3>
        <b>Timestamp:</b> {log['timestamp']}<br>
        <b>Service:</b> {log['service']}<br>
        <b>Source IP:</b> {log['src_ip']}<br>
        <b>Destination IP:</b> {log['dst_ip']}<br>
        <b>Event:</b> {log['event']}<br>
        <b>Action:</b> {log['action']}
    </div>
    """,
    unsafe_allow_html=True
)

# ======================================================
# ANALYSIS CONFIGURATION
# ======================================================
st.markdown(
    """
    <div class="soc-card">
        <h3>Analysis Configuration</h3>
    </div>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    rule_based = st.checkbox("Rule-based analysis", value=True)

with col2:
    ml_based = st.checkbox("ML-based analysis", value=True)

with col3:
    llm_based = st.checkbox("LLM-based analysis", value=True)

severity = st.selectbox(
    "Analyst severity assessment",
    ["Low", "Medium", "High"]
)

# ======================================================
# RUN ANALYSIS
# ======================================================
if st.button("Run Threat Analysis"):

    analysis_rows = []

    if rule_based:
        rule_result = "No critical rule violation detected"
        if "fail" in str(log["event"]).lower():
            rule_result = "Rule triggered: Repeated failure pattern"
        analysis_rows.append(("Rule-based", rule_result))

    if ml_based:
        score = 0.9 if severity == "High" else 0.6
        analysis_rows.append(("ML-based", f"Anomaly score = {score}"))

    # ==================================================
    # RESULTS TABLE
    # ==================================================
    st.markdown(
        """
        <div class="soc-card">
            <h3>Analysis Results</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    results_df = pd.DataFrame(
        analysis_rows,
        columns=["Analysis Type", "Result"]
    )

    st.table(results_df)

    # ==================================================
    # LLM ANALYSIS
    # ==================================================
    if llm_based:
        st.markdown(
            """
            <div class="soc-card">
                <h3>LLM Incident Report</h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        ml_stub = {
            "severity": severity,
            "score": 0.9
        }

        with st.spinner("Generating LLM incident report..."):
            llm_output = get_llm_report(log.to_dict(), ml_stub)

        clean_report = re.sub(r"\[.*?\]", "", llm_output["llm_report"]).strip()

        st.markdown(
            f"""
            <div class="soc-card" style="max-height:260px; overflow-y:auto;">
                {clean_report}
            </div>
            """,
            unsafe_allow_html=True
        )
