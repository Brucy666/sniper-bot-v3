import os
import json
from sniper_test_feed import load_test_feed
from sniper_scoring_engine import score_sniper_candle
from heatmap_engine import detect_heatmap_absorption
from trap_journal import log_sniper_hit

def run_backtest():
    df = load_test_feed()

    results = []
    for i in range(20, len(df)):
        history = df.iloc[i - 20:i].to_dict(orient="records")
        row = df.iloc[i].copy()

        # 🔥 Add heatmap trap detection
        row["heatmap_absorption"] = detect_heatmap_absorption(history)

        # 🧠 Score candle using all enabled logic
        score, tags = score_sniper_candle(row, history)

        if score >= 0.6:
            result = {
                "timestamp": row["timestamp"].isoformat(),
                "entry_price": row["close"],
                "score": score,
                "tags": tags
            }
            print("🎯 SNIPER HIT:", result)
            results.append(result)
            log_sniper_hit(result)

    os.makedirs("logs", exist_ok=True)
    with open("logs/test_sniper_log.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_backtest()
