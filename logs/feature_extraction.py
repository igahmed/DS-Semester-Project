import pandas as pd

def extract_features_from_logs(logs):
    rows = []

    for log in logs:
        hour = int(log['timestamp'][11:13])

        row = {
            # -------- NUMERIC (10) --------
            'dst_port': log['dst_port'],
            'packet_size': log['packet_size'],
            'duration': log['duration'],
            'login_attempts': log['login_attempts'],
            'hour': hour,
            'is_night': int(hour < 6 or hour > 22),
            'is_privileged_port': int(log['dst_port'] < 1024),
            'is_internal_src': int(log['src_ip'].startswith(('10.', '192.168.'))),
            'is_internal_dst': int(log['dst_ip'].startswith(('10.', '192.168.'))),
            'packet_rate': log['packet_size'] / max(log['duration'], 0.1),

            # -------- PROTOCOL (2) --------
            'protocol_TCP': int(log['protocol'] == 'TCP'),
            'protocol_UDP': int(log['protocol'] == 'UDP'),

            # -------- SERVICE (8) --------
            'service_HTTP': int(log['service'] == 'HTTP'),
            'service_HTTPS': int(log['service'] == 'HTTPS'),
            'service_SSH': int(log['service'] == 'SSH'),
            'service_DNS': int(log['service'] == 'DNS'),
            'service_FTP': int(log['service'] == 'FTP'),
            'service_SMTP': int(log['service'] == 'SMTP'),
            'service_RDP': int(log['service'] == 'RDP'),
            'service_OTHER': int(log['service'] not in [
                'HTTP','HTTPS','SSH','DNS','FTP','SMTP','RDP'
            ])
        }

        rows.append(row)

    return pd.DataFrame(rows)



