import numpy as np

def calculate_average_volume(candles, period):
    volumes = [candle['volume'] for candle in candles[-period:]]
    return np.mean(volumes)
