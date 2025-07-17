import requests
import pandas as pd

def fetch_klines(symbol="BTC-USDT", interval="1min", limit=100):
    url = f"https://api.kucoin.com/api/v1/market/candles"
    params = {"symbol": symbol, "type": interval}
    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json().get("data", [])[:limit]
    except:
        return []

def get_kucoin_sniper_feed():
    raw = fetch_klines()
    if not raw:
        return None

    df = pd.DataFrame(raw, columns=[
        "timestamp", "open", "close", "high", "low", "volume", "turnover"
    ])
    df = df.iloc[::-1]
    df[["open", "close", "high", "low", "volume"]] = df[["open", "close", "high", "low", "volume"]].astype(float)
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms", errors="coerce")

    pv = (df["close"] * df["volume"]).cumsum()
    df["vwap"] = pv / df["volume"].cumsum()

    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df
