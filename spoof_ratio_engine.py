def calculate_spoof_ratio(orderbook):
    """
    Given a list of bids/asks, returns spoof ratio.
    :param orderbook: {"bids": [[price, size]], "asks": [[price, size]]}
    :return: float (0.0 to 1.0)
    """
    try:
        total_bids = sum(float(b[1]) for b in orderbook["bids"])
        total_asks = sum(float(a[1]) for a in orderbook["asks"])
        ratio = total_bids / (total_bids + total_asks)
        return round(ratio, 3)
    except:
        return 0.5  # Neutral
