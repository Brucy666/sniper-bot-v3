import pandas as pd

def generate_tpo_profile(df, tick_size=5):
    """
    Create a TPO-like profile from OHLCV candles.
    Returns: dict with POC, VAH, VAL, and price bins.
    """
    price_range = []
    for _, row in df.iterrows():
        levels = list(range(int(row["low"]), int(row["high"]) + tick_size, tick_size))
        price_range.extend(levels)

    tpo_df = pd.Series(price_range)
    profile = tpo_df.value_counts().sort_index()

    total_count = profile.sum()
    value_area = profile[profile.cumsum() <= total_count * 0.7]

    return {
        "poc": profile.idxmax(),
        "vah": value_area.index.max(),
        "val": value_area.index.min(),
        "tpo_count": profile.to_dict()
    }

def is_untested_poc(current_price, known_pocs, tolerance=10):
    return any(abs(current_price - poc) < tolerance for poc in known_pocs)
