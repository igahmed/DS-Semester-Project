from datetime import datetime


class LLMAnalyzer:
    def analyze_threat(self, threat_data):
        severity = threat_data.get("severity", "Low")

        templates = {
            "High": {
                "summary": "Critical security threat detected",
                "details": "Activity strongly deviates from normal behavior and indicates a potential attack.",
                "recommendations": [
                    "Block source IP immediately",
                    "Isolate affected system",
                    "Notify security team",
                    "Preserve logs for investigation"
                ],
                "confidence": "High"
            },
            "Medium": {
                "summary": "Suspicious activity detected",
                "details": "Behavior deviates from baseline and requires further monitoring.",
                "recommendations": [
                    "Increase monitoring",
                    "Review related user activity",
                    "Apply temporary access restrictions if needed"
                ],
                "confidence": "Medium"
            },
            "Low": {
                "summary": "Minor anomaly observed",
                "details": "Slight deviation from expected behavior, likely benign.",
                "recommendations": [
                    "Continue monitoring",
                    "Reassess if pattern repeats"
                ],
                "confidence": "Low"
            }
        }

        result = templates.get(severity, templates["Low"]).copy()

        result["timestamp"] = datetime.utcnow().isoformat()
        result["source"] = "template_llm"

        return result
