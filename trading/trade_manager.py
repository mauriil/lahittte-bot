import time
import logging
from utils.threading import run_in_thread

def place_trade(api, direction, balance, active, risk, candle_size):
    def trade_thread(direction, balance):
        trade_amount = balance * risk
        check, trade_id = api.buy(trade_amount, active, direction.lower(), candle_size // 60)
        if check:
            logging.info(f"Operación realizada: {direction} por ${trade_amount:.2f}. ID: {trade_id}")
            time.sleep(candle_size + 5)
            result, profit = api.check_win_v3(trade_id)
            if result == "win":
                logging.info(f"WIN: Ganancia de ${profit:.2f}")
            elif result == "loss":
                logging.info(f"LOSS: Pérdida de ${trade_amount:.2f}")

    run_in_thread(trade_thread, direction, balance)
