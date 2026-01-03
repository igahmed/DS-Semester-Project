import json
import os
import pandas as pd
from llm.llm_integration import LLMAnalyzer

RULES_FILE = "config/threat_rules.json"
LOG_FILE = "logs/logs.csv"


def load_rules():
    if not os.path.exists(RULES_FILE):
        return {}
    with open(RULES_FILE, "r") as f:
        return json.load(f)


def analyze_threats(use_ml=True, use_llm=True, manual_rules=True):
    if not os.path.exists(LOG_FILE):
        return {"status": "No logs found"}

    df = pd.read_csv(LOG_FILE, on_bad_lines="skip")

    if df.empty:
        return {"status": "No logs to analyze"}

    rules = load_rules()
    analyzer = LLMAnalyzer()

    severity_counts = {"Low": 0, "Medium": 0, "High": 0}
    analyzed_events = []

    for _, row in df.iterrows():
        severity = "Low"
        reason = "Normal system behavior"

        if manual_rules:
            if row.get("login_attempts", 0) >= rules.get("failed_logins", {}).get("threshold", 5):
                severity = "High"
                reason = "Multiple failed authentication attempts detected"

            else:
                try:
                    hour = int(str(row.get("timestamp"))[11:13])
                    if hour >= 22 or hour < 5:
                        severity = "Medium"
                        reason = "Activity observed during unusual hours"
                except Exception:
                    pass

        severity_counts[severity] += 1

        analyzed_events.append({
            "timestamp": row.get("timestamp"),
            "service": row.get("service"),
            "src_ip": row.get("src_ip"),
            "dst_ip": row.get("dst_ip"),
            "severity": severity,
            "reason": reason
        })

    report = {}

    if use_llm:
        for level in ["Low", "Medium", "High"]:
            report[level] = analyzer.analyze_threat({
                "severity": level
            })

    return {
        "status": "Analysis completed",
        "summary": severity_counts,
        "events": analyzed_events[-10:],
        "llm_report": report
    }
