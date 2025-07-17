import json
from datetime import datetime
from bybit_feed import get_bybit_sniper_feed
import pandas as pd

def detect_rsi_vsplit(df):
    rsi_vals = df['rsi'].iloc[-3:].tolist()
    if len(rsi_vals) < 3 or any(pd.isnull(rsi_vals)):
        return False
    rsi1, rsi2, rsi3 = rsi_vals
    return rsi1 > rsi2 < rsi3 and rsi3 > 30

def detect_vwap_trap(df):
    try:
        close = float(df['close'].iloc[-1])
        vwap = float(df['vwap'].iloc[-1])
        return close < vwap
    except:
        return False

def run_bybit_sniper_scan():
    df = get_bybit_sniper_feed()
    if df is None or len(df) < 20:
        return

    if detect_rsi_vsplit(df) and detect_vwap_trap(df):
        signal = {
            "exchange": "Bybit",
            "symbol": "BTCUSDT",
            "timestamp": datetime.utcnow().isoformat(),
            "entry_price": float(df['close'].iloc[-1]),
            "vwap": float(df['vwap'].iloc[-1]),
            "rsi": float(df['rsi'].iloc[-1]),
            "reason": "RSI-V + VWAP Trap",
            "score": 1.0
        }
        with open("logs/bybit_sniper.json", "a") as f:
            f.write(json.dumps(signal) + "\n")
        print("[BYBIT SNIPER] Signal Triggered:", signal)
    else:
        print("[BYBIT SNIPER] No sniper setup.")
