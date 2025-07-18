def detect_heatmap_absorption(candles, threshold=2.0):
    """
    Looks at last few candles and flags high-volume zones where price stalls.
    """
    recent = candles[-3:]
    avg_volume = sum(c["volume"] for c in candles[-20:]) / 20

    for c in recent:
        if c["volume"] > threshold * avg_volume and abs(c["close"] - c["open"]) < 10:
            return True

    return False
