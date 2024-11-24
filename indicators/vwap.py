def calculate_vwap(candles):
    typical_prices = [(candle['high'] + candle['low'] + candle['close']) / 3 for candle in candles]
    volumes = [candle['volume'] for candle in candles]
    vwap = sum(tp * v for tp, v in zip(typical_prices, volumes)) / sum(volumes)
    return vwap
