import numpy as np

def calculate_bollinger_bands(prices, period=20):
    sma = np.mean(prices[-period:])
    std_dev = np.std(prices[-period:])
    upper_band = sma + 2 * std_dev
    lower_band = sma - 2 * std_dev
    return upper_band, sma, lower_band
