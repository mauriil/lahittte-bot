from indicators.ema import calculate_ema

def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    ema_short = calculate_ema(prices, short_period)
    ema_long = calculate_ema(prices, long_period)
    macd_line = ema_short - ema_long
    signal_line = calculate_ema([macd_line], signal_period)
    return macd_line, signal_line
