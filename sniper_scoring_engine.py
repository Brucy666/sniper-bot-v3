def score_sniper_candle(row):
    confluence = []
    score = 0

    if row.get("rsi") and row["rsi"] < 35:
        score += 0.3
        confluence.append("RSI-V")

    if row.get("close") < row.get("vwap", 0):
        score += 0.3
        confluence.append("Below VWAP")

    if row.get("spoof_ratio", 0) > 0.9:
        score += 0.2
        confluence.append("Spoof High")

    if row.get("cvd_divergence", False):
        score += 0.2
        confluence.append("CVD Divergence")

    return round(score, 2), confluence
