# mock_data_runner.py
# Feeds historical BTC/USDT data bar-by-bar into the sniper engine for backtesting

import pandas as pd
import time
from sniper_backtest_engine import process_candle

# Load historical data (CSV committed to root repo)
data_path = "btc_usdt_1m_backtest_full_july2025.csv"
df = pd.read_csv(data_path, parse_dates=['timestamp'])

# Loop through candles like it's a live feed
for idx, row in df.iterrows():
    candle = {
        'timestamp': row['timestamp'],
        'open': float(row['open']),
        'high': float(row['high']),
        'low': float(row['low']),
        'close': float(row['close']),
        'volume': float(row['volume'])
    }
    process_candle(candle)
    time.sleep(0.01)  # Simulate real-time speed (adjust for faster/lower CPU usage)

print("Backtest complete.")
