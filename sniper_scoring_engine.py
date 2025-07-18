from cvd_divergence import detect_cvd_divergence
from spoof_ratio_engine import calculate_spoof_ratio
from trap_memory import check_reentry

def score_sniper_candle(row, history, orderbook=None):
    """
    Score a single candle using multiple confluence tools.
    Returns: (score: float, tags: list[str])
    """

    score = 0
    tags = []

    # --- RSI-V Split Detection ---
    try:
        rsi_vals = [h["rsi"] for h in history[-3:]] + [row["rsi"]]
        if rsi_vals[0] > rsi_vals[1] < rsi_vals[2] and rsi_vals[3] > 30:
            score += 0.25
            tags.append("RSI-V Split")
    except:
        pass

    # --- VWAP Trap Zone ---
    try:
        if row["close"] < row["vwap"]:
            score += 0.20
            tags.append("Below VWAP")
    except:
        pass

    # --- Spoof Ratio from Orderbook ---
    if orderbook:
        spoof_ratio = calculate_spoof_ratio(orderbook)
        row["spoof_ratio"] = spoof_ratio
        if spoof_ratio > 0.85:
            score += 0.20
            tags.append("Spoof Ratio High")

    # --- CVD Divergence Detection ---
    try:
        price_series = [h["close"] for h in history[-3:]] + [row["close"]]
        cvd_series = [h.get("cvd", 0) for h in history[-3:]] + [row.get("cvd", 0)]
        if detect_cvd_divergence(price_series, cvd_series):
            score += 0.20
            tags.append("CVD Divergence")
    except:
        pass

    # --- Heatmap Absorption (Volume Spike with Stalled Candle) ---
    if row.get("heatmap_absorption", False):
        score += 0.10
        tags.append("Heatmap Trap")

    # --- Reentry into Old Trap Zones ---
    if check_reentry(row["close"]):
        score += 0.10
        tags.append("Reentry Trap")

    # --- Optional: TPO Untested POC Support ---
    if row.get("tpo_zone") == "untested_poc":
        score += 0.10
        tags.append("Untested POC")

    return round(score, 2), tags
