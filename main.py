import logging
import time
from trading.config import *
from trading.market_analysis import analyze_market
from trading.trade_manager import place_trade
from utils.logger import setup_logger
from my_iqoptionapi.stable_api import IQ_Option

def main():
    setup_logger()
    logging.info("Iniciando bot de trading")
    api = IQ_Option(EMAIL, PASSWORD)
    api.connect()
    api.change_balance(BALANCE_TYPE)

    trades_done = 0
    balance = api.get_balance()

    while trades_done < MAX_TRADES:
        if not api.check_connect():
            api.connect()

        direction = analyze_market(api, ACTIVES, CANDLE_SIZE, PERIODS)
        if direction:
            place_trade(api, direction, balance, ACTIVES, RISK, CANDLE_SIZE)
            trades_done += 1

        time.sleep(60)

if __name__ == "__main__":
    main()
