from cvd_divergence import detect_cvd_divergence
from spoof_ratio_engine import calculate_spoof_ratio

def score_sniper_candle(row, history, orderbook=None):
    """
    Scores a candle using RSI-V, VWAP trap, CVD divergence, and spoof ratio.
    - `row`: current candle (dict or Series)
    - `history`: previous candles (DataFrame or list of dicts)
    - `orderbook`: optional live bid/ask snapshot
    """

    confluence = []
    score = 0

    # --- RSI-V ---
    try:
        rsi_vals = [h["rsi"] for h in history[-3:]] + [row["rsi"]]
        if rsi_vals[0] > rsi_vals[1] < rsi_vals[2] and rsi_vals[3] > 30:
            score += 0.25
            confluence.append("RSI-V Split")
    except:
        pass

    # --- VWAP Trap ---
    try:
        if row["close"] < row["vwap"]:
            score += 0.2
            confluence.append("Below VWAP")
    except:
        pass

    # --- Spoof Ratio ---
    if orderbook:
        spoof_ratio = calculate_spoof_ratio(orderbook)
        row["spoof_ratio"] = spoof_ratio
        if spoof_ratio > 0.85:
            score += 0.2
            confluence.append("Spoof Ratio High")

    # --- CVD Divergence ---
    try:
        price_hist = [h["close"] for h in history[-3:]] + [row["close"]]
        cvd_hist = [h.get("cvd", 0) for h in history[-3:]] + [row.get("cvd", 0)]
        if detect_cvd_divergence(price_hist, cvd_hist):
            score += 0.2
            confluence.append("CVD Divergence")
    except:
        pass

    # --- TPO + Heatmap Hooks (future use) ---
    if row.get("tpo_zone") == "untested_poc":
        score += 0.1
        confluence.append("Untested POC")

    if row.get("heatmap_absorption", False):
        score += 0.1
        confluence.append("Heatmap Trap")

    # Final scoring
    return round(score, 2), confluence
