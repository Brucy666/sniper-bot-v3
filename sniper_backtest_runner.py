import os
import json
from sniper_test_feed import load_test_feed
from sniper_scoring_engine import score_sniper_candle

def run_backtest():
    df = load_test_feed()

    results = []
    for i in range(20, len(df)):
        row = df.iloc[i]
        score, tags = score_sniper_candle(row)

        if score >= 0.6:
            result = {
                "timestamp": row["timestamp"].isoformat(),
                "entry_price": row["close"],
                "score": score,
                "tags": tags
            }
            results.append(result)
            print("🎯 SNIPER HIT:", result)

    os.makedirs("logs", exist_ok=True)
    with open("logs/test_sniper_log.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_backtest()
