from client import Client
from json import loads
from datetime import datetime
import ssl
import requests


class Binance(Client):
    def __init__(self, url, exchange, last_prices, orderbook, lock):
        super().__init__(url, exchange)

        # local data management
        self.orderbook = orderbook[exchange]
        self.lock = lock
        self.updates = 0
        self.last_update = orderbook
        self.last_prices=last_prices

    # convert message to dict, process update
    def on_message(self,_ , message):
        data = loads(message)



        ticker = data.get('s').lower()
        if self.last_prices.get(ticker).get('updateId', 0) < data.get('u'):
            self.update_last_prices(data=data)


        # check for orderbook, if empty retrieve
        # if len(self.orderbook) == 0:
        #     for key, value in self.get_snapshot().items():
        #         self.orderbook[key] = value
        #
        #
        #
        # # get lastUpdateId
        # lastUpdateId = self.orderbook['lastUpdateId']
        #
        # # drop any updates older than the snapshot
        # if self.updates == 0:
        #     if data['U'] <= lastUpdateId+1 and data['u'] >= lastUpdateId+1:
        #         self.orderbook['lastUpdateId'] = data['u']
        #         self.process_updates(data)
        #
        #
        #
        # # check if update still in sync with orderbook
        # elif data['U'] == lastUpdateId+1:
        #     self.orderbook['lastUpdateId'] = data['u']
        #     self.process_updates(data)
        # else:
        #     print('Out of sync, abort')

    def update_last_prices(self, data):
        with self.lock:
            ## update last_prices
            mid = (float(data['b']) + float(data['a']) )/2
            ticker = data.get('s').lower()
            self.last_prices[ticker]['mid'] = mid
            self.last_prices['timestamp'] = datetime.now().timestamp()
            self.last_prices[ticker]['updateId']= data['u']

    # # Loop through all bid and ask updates, call manage_orderbook accordingly
    # def process_updates(self, data):
    #     with self.lock:
    #         for update in data['b']:
    #             self.manage_orderbook('bids', update)
    #         for update in data['a']:
    #             self.manage_orderbook('asks', update)
    #         self.last_update['last_update'] = datetime.now()

    # # Update orderbook, differentiate between remove, update and new
    # def manage_orderbook(self, side, update):
    #     # extract values
    #     price, qty = update
    #
    #     # loop through orderbook side
    #     for x in range(0, len(self.orderbook[side])):
    #         if price == self.orderbook[side][x][0]:
    #             # when qty is 0 remove from orderbook, else
    #             # update values
    #             if qty == 0:
    #                 del self.orderbook[side]
    #                 break
    #             else:
    #                 self.orderbook[side][x] = update
    #                 break
    #         # if the price level is not in the orderbook,
    #         # insert price level, filter for qty 0
    #         elif ((price > self.orderbook[side][x][0] and side == 'bids') or
    #                 (price < self.orderbook[side][x][0] and side == 'asks')):
    #             if qty != 0:
    #                 self.orderbook[side].insert(x, update)
    #                 break
    #             else:
    #                 break
    #
    # # retrieve orderbook snapshot
    # def get_snapshot(self):
    #     r = requests.get('https://www.binance.com/api/v1/depth?symbol=STEEMBTC&limit=1000')
    #     return loads(r.content.decode())