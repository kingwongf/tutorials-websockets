from binance import Binance
from huobi import Huobi
from datetime import datetime
import threading
import time


# print top bid/ask for each exchange
# run forever
def run(orderbooks, last_prices, lock,):
    # local last_update
    current_time = datetime.now().timestamp()

    while True:
        try:
            # check for new update
            # if orderbooks['last_update'] != current_time:
            #     with lock:
            #         # extract and print data
            #         for key, value in orderbooks.items():
            #             if key != 'last_update':
            #                 pass
            #                 bid = value['bids'][0][0]
            #                 ask = value['asks'][0][0]
            #                 print(f"{key} bid: {bid} ask: {ask}")
            #         print()
            #
            #         # set local last_update to last_update
            #         current_time = orderbooks['last_update']

            if last_prices['timestamp'] != current_time:
                with lock:
                    # extract and print data
                    print(last_prices)
                    print()

                    # set local last_update to last_update
                    current_time = last_prices['timestamp']
            # time.sleep(0.1)
        except Exception:
            pass


if __name__ == "__main__":
    # data management
    lock = threading.Lock()
    orderbooks = {
        "Binance": {},
        "Huobi": {},
        "last_update": None,
    }

    last_prices = {
        "btcusdt": {'updateId': 0, 'mid': None},
        "ethusdt": {'updateId': 0, 'mid': None}
    }

    # create websocket threads
    # binance_btcusdt = Binance(
    #     url="wss://stream.binance.com:9443/ws/btcusdt@depth",
    #     exchange="Binance",
    #     orderbook=orderbooks,
    #     lock=lock,
    # )

    binance_btcusdt = Binance(
        url="wss://stream.binance.com:9443/ws/btcusdt@bookTicker",
        exchange="Binance",
        orderbook=orderbooks,
        last_prices=last_prices,
        lock=lock,
    )

    binance_ethusdt = Binance(
        url="wss://stream.binance.com:9443/ws/ethusdt@bookTicker",
        exchange="Binance",
        orderbook=orderbooks,
        last_prices=last_prices,
        lock=lock,
    )

    # huobi = Huobi(
    #     url="wss://api.huobipro.com/ws",
    #     exchange="Huobi",
    #     orderbook=orderbooks,
    #     lock=lock,
    # )

    # start threads
    binance_btcusdt.start()
    binance_ethusdt.start()
    # huobi.start()

    # process websocket data
    run(orderbooks, last_prices, lock)