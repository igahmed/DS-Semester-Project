import pandas as pd
import random
import time
from datetime import datetime
import os
from threading import Thread

LOG_FILE = "logs/logs.csv"
os.makedirs("logs", exist_ok=True)

SERVICES = {
    80: "HTTP",
    443: "HTTPS",
    22: "SSH",
    21: "FTP",
    53: "DNS",
    3389: "RDP",
    445: "SMB"
}

PROTOCOLS = ["TCP", "UDP"]


def random_private_ip():
    choice = random.choice(["192", "10", "172"])

    if choice == "192":
        return f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}"

    if choice == "10":
        return f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    return f"172.{random.randint(16, 31)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def random_public_ip():
    return f"{random.randint(11, 223)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"


def generate_logs():
    while True:
        dst_port = random.choice(list(SERVICES.keys()))
        service = SERVICES[dst_port]

        src_private = random.choices([True, False], weights=[0.7, 0.3])[0]

        log = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "src_ip": random_private_ip() if src_private else random_public_ip(),
            "dst_ip": random_private_ip(),
            "dst_port": dst_port,
            "protocol": random.choice(PROTOCOLS),
            "packet_size": random.randint(200, 9000),
            "duration": round(random.uniform(0.05, 8.0), 2),
            "service": service,
            "login_attempts": (
                random.randint(0, 15) if service in ["SSH", "RDP", "FTP"] else 0
            )
        }

        df = pd.DataFrame([log])
        df.to_csv(
            LOG_FILE,
            mode="a",
            header=not os.path.exists(LOG_FILE),
            index=False
        )

        time.sleep(random.randint(5, 12))


def start_log_generator():
    Thread(target=generate_logs, daemon=True).start()
