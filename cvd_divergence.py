def detect_cvd_divergence(prices, cvd_values):
    """
    Detects divergence where price makes higher high but CVD does not.
    :param prices: List of closing prices
    :param cvd_values: List of CVD values (same length)
    :return: True if divergence detected
    """
    if len(prices) < 3 or len(cvd_values) < 3:
        return False

    # Price makes higher high
    if prices[-1] > prices[-2] > prices[-3]:
        # CVD fails to follow
        if cvd_values[-1] < cvd_values[-2]:
            return True

    return False
