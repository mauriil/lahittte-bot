import time
import logging
from indicators.ema import calculate_ema
from indicators.rsi import calculate_rsi
from indicators.bollinger_bands import calculate_bollinger_bands
from indicators.volume import calculate_average_volume
from notifiers.telegram_notifier import TelegramNotifier

# Configuración del logger
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

bot_token = "7708653394:AAHhksu4audsYeaPaM8USjzsyaWdQcnYrj4"
chat_id = "961277363"
notifier = TelegramNotifier(bot_token, chat_id)

def analyze_market(api, active, candle_size, periods):
    """
    Analiza el mercado utilizando múltiples indicadores técnicos para determinar si operar.
    """
    try:
        # Obtener velas
        candles = api.get_candles(active, candle_size, 20, time.time())
        if len(candles) < periods:
            logging.warning("No hay suficientes velas para el análisis.")
            return None

        # Extraer precios y volumen
        prices = [candle['close'] for candle in candles]
        volumes = [candle.get('volume', 0) for candle in candles]
        avg_volume = calculate_average_volume(candles, periods)

        # Calcular indicadores
        ema_fast = calculate_ema(prices, 5)
        ema_slow = calculate_ema(prices, 20)
        rsi = calculate_rsi(prices, 14)
        bollinger_upper, bollinger_middle, bollinger_lower = calculate_bollinger_bands(prices, periods)

        # Inicializar puntaje
        score = 0

        # Parámetros de velas
        last_candle = candles[-1]
        second_last_candle = candles[-2]

        # Vela alcista o bajista
        if last_candle['close'] > last_candle['open']:
            score += 1  # Vela alcista
        elif last_candle['close'] < last_candle['open']:
            score -= 1  # Vela bajista

        # Tamaño de la vela
        last_candle_size = last_candle['max'] - last_candle['min']
        if last_candle_size > 0.0002:  # Ajusta el umbral según el mercado
            score += 1  # Movimiento fuerte
        elif last_candle_size < 0.0001:
            score -= 1  # Movimiento débil

        # Relación cuerpo/sombra
        body_size = abs(last_candle['close'] - last_candle['open'])
        shadow_size = last_candle_size - body_size
        if body_size > shadow_size:
            score += 1  # Cuerpo dominante
        elif shadow_size > body_size:
            score -= 1  # Sombras dominantes

        # Secuencia de velas
        if last_candle['close'] > last_candle['open'] and second_last_candle['close'] > second_last_candle['open']:
            score += 1  # Dos velas alcistas consecutivas
        elif last_candle['close'] < last_candle['open'] and second_last_candle['close'] < second_last_candle['open']:
            score -= 1  # Dos velas bajistas consecutivas

        # Indicadores técnicos
        if ema_fast > ema_slow:
            score += 2  # Tendencia alcista
        if ema_fast < ema_slow:
            score -= 2  # Tendencia bajista

        if rsi < 30:
            score += 1  # Condición de sobreventa
        if rsi > 70:
            score -= 1  # Condición de sobrecompra

        if prices[-1] < bollinger_lower:
            score += 1  # Precio por debajo de la banda inferior
        if prices[-1] > bollinger_upper:
            score -= 1  # Precio por encima de la banda superior

        if volumes[-1] > avg_volume * 0.5:
            score += 1  # Volumen significativo

        # Logging de diagnóstico
        logging.debug(f"Score: {score}")
        logging.debug(f"EMA Fast: {ema_fast}, EMA Slow: {ema_slow}, RSI: {rsi}")
        logging.debug(f"Bollinger: {bollinger_lower}-{bollinger_upper}")
        logging.debug(f"Last Candle: {last_candle}, Avg Volume: {avg_volume}")

        # Decidir acción
        if score >= 3:
            notifier.send_message(f"CALL detected on {active} with score {score}")
            return "CALL"
        elif score <= -3:
            notifier.send_message(f"PUT detected on {active} with score {score}")
            return "PUT"
        else:
            return None

    except Exception as e:
        logging.error(f"Error al analizar el mercado: {e}")
        notifier.send_message(f"Error in analyze_market: {e}")
        return None

