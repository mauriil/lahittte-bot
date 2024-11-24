
def is_hammer(candle):
    body = candle['close'] - candle['open']
    tail = candle['low'] - min(candle['close'], candle['open'])
    return tail > abs(body) * 2 and body > 0

def is_shooting_star(candle):
    body = candle['close'] - candle['open']
    shadow = candle['high'] - max(candle['close'], candle['open'])
    return shadow > abs(body) * 2 and body < 0
