def calculate_atr(candles, period=14):
    tr_values = [
        max(candle['high'] - candle['low'],
            abs(candle['high'] - candles[i-1]['close']),
            abs(candle['low'] - candles[i-1]['close']))
        for i, candle in enumerate(candles[1:], start=1)
    ]
    return sum(tr_values[-period:]) / period
