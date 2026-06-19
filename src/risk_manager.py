def calculate_position_size(balance, risk_per_trade, entry, stop_loss):
    risk_amount = balance * risk_per_trade
    price_risk = abs(entry - stop_loss)

    if price_risk == 0:
        return 0

    return round(risk_amount / price_risk, 6)


def calculate_trade_risk(balance, risk_per_trade):
    return round(balance * risk_per_trade, 2)


def is_risk_allowed(risk_per_trade, max_risk_per_trade=0.02):
    return 0 < risk_per_trade <= max_risk_per_trade
