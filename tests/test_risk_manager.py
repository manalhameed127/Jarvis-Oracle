from src.risk_manager import (
    calculate_position_size,
    calculate_trade_risk,
    is_risk_allowed
)


position_size = calculate_position_size(
    balance=100,
    risk_per_trade=0.01,
    entry=100,
    stop_loss=95
)

print("Position Size:", position_size)
print("Risk Amount:", calculate_trade_risk(100, 0.01))
print("Risk Allowed:", is_risk_allowed(0.01))
print("Too Much Risk Allowed:", is_risk_allowed(0.05))
