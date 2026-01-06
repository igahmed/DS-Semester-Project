import sys
import os
import joblib

# ======================================================
# CRITICAL: RESTORE OLD PIPELINE IMPORT PATH
# ======================================================
# This is required because pipeline.pkl was trained with:
# from feature_extraction import extract_features_from_logs

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

from logs.feature_extraction import extract_features_from_logs

PIPELINE_PATH = "models/pipeline.pkl"
MODEL_PATH = "models/isolation_forest.pkl"


class MLPredictor:
    def __init__(self):
        self.pipeline = joblib.load(PIPELINE_PATH)
        self.model = joblib.load(MODEL_PATH)

    def predict(self, log_dict):
        X = self.pipeline.transform([log_dict])

        score = float(self.model.decision_function(X)[0])
        prediction = int(self.model.predict(X)[0])

        severity = "High" if prediction == -1 else "Low"

        return {
            "severity": severity,
            "score": round(score, 4),
            "decision": "Anomaly" if prediction == -1 else "Normal"
        }
