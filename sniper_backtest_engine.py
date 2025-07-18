# sniper_backtest_engine.py
# Detects sniper trap logic on each candle and logs the outcome

from trap_journal import log_sniper_event
import pandas as pd

# RSI-V Split Detector (3-bar pattern)
def detect_rsi_vsplit(history):
    if len(history) < 3:
        return False
    rsi1, rsi2, rsi3 = history[-3:]
    return rsi1 > rsi2 < rsi3 and rsi3 > 30

# VWAP Trap Detector (price under VWAP)
def detect_vwap_trap(close, vwap):
    return close < vwap

# Placeholder VWAP calculator (rolling mean for demo)
def calc_vwap(price_list, volume_list):
    pv = [p * v for p, v in zip(price_list, volume_list)]
    return sum(pv) / sum(volume_list) if sum(volume_list) != 0 else 0

# Historical RSI calculator (naive 14-period)
def calc_rsi(prices, period=14):
    if len(prices) < period:
        return None
    delta = pd.Series(prices).diff()
    gain = delta.where(delta > 0, 0).rolling(window=period).mean()
    loss = -delta.where(delta < 0, 0).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

# Price and volume buffer for rolling calculations
price_buffer = []
volume_buffer = []
rsi_buffer = []

# Main processing function for each candle
def process_candle(candle):
    price_buffer.append(candle['close'])
    volume_buffer.append(candle['volume'])
    
    if len(price_buffer) < 15:
        return

    rsi = calc_rsi(price_buffer)
    if rsi is None:
        return

    rsi_buffer.append(rsi)
    vwap = calc_vwap(price_buffer, volume_buffer)
    
    rsi_trigger = detect_rsi_vsplit(rsi_buffer)
    vwap_trigger = detect_vwap_trap(candle['close'], vwap)

    if rsi_trigger and vwap_trigger:
        score = 1.0
        event = {
            "timestamp": str(candle['timestamp']),
            "entry_price": candle['close'],
            "vwap": round(vwap, 2),
            "rsi": round(rsi, 2),
            "reason": "RSI-V + VWAP Trap",
            "score": score
        }
        log_sniper_event(event)
        print("[SNIPER BACKTEST] Triggered:", event)
