import json
import os
from huggingface_hub import InferenceClient


HF_TOKEN = "API_KEY"
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

client = InferenceClient(
    model=MODEL_NAME,
    token=HF_TOKEN,
    timeout=60
)



def build_prompt(log_data, ml_result):
    return f"""
You are an AI cybersecurity assistant embedded in a SOC dashboard.

Write a SHORT, human-readable incident report.

STRICT RULES:
- Do NOT include instructions, roles, or log context
- Do NOT include IPs unless necessary
- First line must be a plain English description
- Follow the exact order below
- Keep it concise and professional

Use this format ONLY:

<Human-readable incident description>

Severity: {ml_result['severity']}

Reason:
<1 short sentence>

Recommendation:
<1 short sentence>

Event description:
{log_data.get("event")}
Action taken:
{log_data.get("action")}
"""



def generate_threat_report(log_data, ml_result):
    prompt = build_prompt(log_data, ml_result)

    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an AI SOC assistant that writes concise incident reports only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        max_tokens=160,
        temperature=0.2
    )

    content = response.choices[0].message.content.strip()

    # 🧹 SAFETY CLEANUP (removes leaked tokens if model misbehaves)
    for token in ["[USER]", "[ASSISTANT]", "[/ASS]", "In"]:
        content = content.replace(token, "").strip()

    return {
        "severity": ml_result["severity"],
        "anomaly_score": ml_result["score"],
        "llm_report": content
    }


def get_llm_report(log_data, ml_output):
    return generate_threat_report(log_data, ml_output)


if __name__ == "__main__":
    sample_log = {
        "timestamp": "2024-06-21 14:33:10",
        "event": "Multiple failed login attempts"
    }

    ml_output = {
        "severity": "High",
        "score": 0.97
    }

    print(json.dumps(generate_threat_report(sample_log, ml_output), indent=2))
