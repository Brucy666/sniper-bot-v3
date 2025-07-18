def simulate_trade(entry_price, candles_after, tp_pct=0.015, sl_pct=0.01):
    """
    Simulates trade outcome based on future candles.
    :param entry_price: float
    :param candles_after: list of dicts with high/low/close
    :return: {"exit_price", "exit_reason", "pnl_pct", "duration"}
    """
    take_profit = entry_price * (1 + tp_pct)
    stop_loss = entry_price * (1 - sl_pct)

    for i, c in enumerate(candles_after):
        high = c["high"]
        low = c["low"]

        if high >= take_profit:
            return {
                "exit_price": take_profit,
                "exit_reason": "TP",
                "pnl_pct": round((take_profit - entry_price) / entry_price * 100, 2),
                "duration": i + 1
            }
        elif low <= stop_loss:
            return {
                "exit_price": stop_loss,
                "exit_reason": "SL",
                "pnl_pct": round((stop_loss - entry_price) / entry_price * 100, 2),
                "duration": i + 1
            }

    # Fallback: close at last known price
    final_price = candles_after[-1]["close"]
    pnl = round((final_price - entry_price) / entry_price * 100, 2)
    return {
        "exit_price": final_price,
        "exit_reason": "Time",
        "pnl_pct": pnl,
        "duration": len(candles_after)
    }
