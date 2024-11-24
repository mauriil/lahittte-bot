from indicators.ema import calculate_ema

def calculate_macd(prices, short_period=12, long_period=26, signal_period=9):
    """
    Calcula la línea MACD y la línea de señal.
    """
    ema_short = [calculate_ema(prices[:i+1], short_period) for i in range(len(prices))]
    ema_long = [calculate_ema(prices[:i+1], long_period) for i in range(len(prices))]
    macd_line = [short - long for short, long in zip(ema_short, ema_long)]

    # Línea de señal: EMA de la línea MACD
    signal_line = [calculate_ema(macd_line[:i+1], signal_period) for i in range(len(macd_line))]

    return macd_line, signal_line
