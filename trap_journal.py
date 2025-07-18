import json
import os

def log_sniper_hit(entry_data):
    os.makedirs("logs", exist_ok=True)
    file_path = "logs/trap_journal.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            log = json.load(f)
    else:
        log = []

    log.append(entry_data)

    with open(file_path, "w") as f:
        json.dump(log, f, indent=2)
