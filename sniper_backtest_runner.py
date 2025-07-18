import os
import json
from sniper_test_feed import load_test_feed
from sniper_scoring_engine import score_sniper_candle
from heatmap_engine import detect_heatmap_absorption
from trap_journal import log_sniper_hit
from trap_memory import remember_trap_zone, check_reentry
from execution_simulator import simulate_trade

def run_backtest():
    df = load_test_feed()
    results = []

    for i in range(20, len(df) - 10):  # leave 10 candles for exit simulation
        history = df.iloc[i - 20:i].to_dict(orient="records")
        row = df.iloc[i].copy()

        # 🔥 Add heatmap signal
        row["heatmap_absorption"] = detect_heatmap_absorption(history)

        # 🧠 Score the candle
        score, tags = score_sniper_candle(row, history)

        # 🧠 Trap memory handling
        if score > 0.7:
            remember_trap_zone(row["close"])
        elif check_reentry(row["close"]):
            row["reentry_trap"] = True
            tags.append("Reentry Trap")
            score += 0.1

        if score >= 0.6:
            # 🧪 Simulate exit outcome
            future = df.iloc[i + 1:i + 11].to_dict(orient="records")
            exit_data = simulate_trade(row["close"], future)

            result = {
                "timestamp": row["timestamp"].isoformat(),
                "entry_price": row["close"],
                "score": round(score, 2),
                "tags": tags,
                **exit_data
            }

            print("🎯 SNIPER HIT:", result)
            results.append(result)
            log_sniper_hit(result)

    os.makedirs("logs", exist_ok=True)
    with open("logs/test_sniper_log.json", "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    run_backtest()
