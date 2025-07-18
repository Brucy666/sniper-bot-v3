import pandas as pd

def load_test_feed(csv_path="data/sample_feed.csv", limit=1000):
    df = pd.read_csv(csv_path)
    df = df[["timestamp", "open", "high", "low", "close", "volume"]].copy()
    df = df.tail(limit)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df[["open", "high", "low", "close", "volume"]] = df[["open", "high", "low", "close", "volume"]].astype(float)

    # VWAP
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()

    # RSI
    delta = df["close"].diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean()
    rs = gain / loss
    df["rsi"] = 100 - (100 / (1 + rs))

    return df
