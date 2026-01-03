import time
import os
import pandas as pd
from datetime import datetime

from models.ml_integration import MLPredictor
from llm.llm import get_llm_report

LOG_FILE = "logs/logs.csv"
INCIDENT_FILE = "logs/incidents.csv"

LLM_COOLDOWN_SECONDS = 60
LAST_LLM_CALL_FILE = "logs/last_llm_call.txt"


def _can_call_llm():
    if not os.path.exists(LAST_LLM_CALL_FILE):
        return True

    with open(LAST_LLM_CALL_FILE, "r") as f:
        last_ts = float(f.read().strip())

    return (time.time() - last_ts) >= LLM_COOLDOWN_SECONDS


def _update_llm_timestamp():
    with open(LAST_LLM_CALL_FILE, "w") as f:
        f.write(str(time.time()))


def consume_logs():
    predictor = MLPredictor()

    while True:
        if not os.path.exists(LOG_FILE):
            time.sleep(1)
            continue

        try:
            logs_df = pd.read_csv(LOG_FILE, on_bad_lines="skip", engine="python")
        except Exception:
            time.sleep(1)
            continue

        if logs_df.empty:
            time.sleep(1)
            continue

        last_log = logs_df.iloc[-1].to_dict()

        ml_result = predictor.predict(last_log)

        is_high = ml_result["severity"] == "High"
        is_suspicious = ml_result["score"] < -0.05

        if not (is_high or is_suspicious):
            time.sleep(2)
            continue

        if not _can_call_llm():
            time.sleep(2)
            continue

        llm_output = get_llm_report(last_log, ml_result)

        incident = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": last_log.get("service"),
            "src_ip": last_log.get("src_ip"),
            "dst_ip": last_log.get("dst_ip"),
            "severity": llm_output["severity"],
            "score": llm_output["anomaly_score"],
            "llm_report": llm_output["llm_report"]
        }

        incident_df = pd.DataFrame([incident])

        write_header = not os.path.exists(INCIDENT_FILE)
        incident_df.to_csv(
            INCIDENT_FILE,
            mode="a",
            header=write_header,
            index=False
        )

        _update_llm_timestamp()
        time.sleep(2)


def start_log_consumer():
    import threading
    t = threading.Thread(target=consume_logs, daemon=True)
    t.start()
