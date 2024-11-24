import numpy as np

def calculate_ema(prices, period):
    ema = [np.mean(prices[:period])]
    multiplier = 2 / (period + 1)
    for price in prices[period:]:
        ema.append((price - ema[-1]) * multiplier + ema[-1])
    return ema[-1]
