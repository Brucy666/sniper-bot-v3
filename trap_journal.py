# trap_journal.py
# Appends sniper events to a trap log CSV

import csv
import os

log_file = "logs/sniper_trap_journal.csv"
os.makedirs("logs", exist_ok=True)

# Create header if file doesn’t exist
if not os.path.exists(log_file):
    with open(log_file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "entry_price", "vwap", "rsi", "reason", "score"])

# Function to log sniper event
def log_sniper_event(event):
    with open(log_file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            event["timestamp"],
            event["entry_price"],
            event["vwap"],
            event["rsi"],
            event["reason"],
            event["score"]
        ])
