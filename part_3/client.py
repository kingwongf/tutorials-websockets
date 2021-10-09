import websocket
import requests
import threading
import ssl
import certifi
from json import loads




class Client(threading.Thread):
    def __init__(self, url, exchange):
        super().__init__()
        # create websocket connection
        self.ws = websocket.WebSocketApp(
            url=url,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )

        # exchange name
        self.exchange = exchange

    # keep connection alive
    def run(self):
        while True:
            # self.ws.run_forever(sslopt={"cert_reqs": CERT_REQUIRED})
            self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE,
                                        "check_hostname": False,
                                        "ssl_version": ssl.PROTOCOL_TLSv1})

    # convert message to dict, process update
    def on_message(self, _, message):
        pass

    # catch errors
    def on_error(self, _, error):
        print("on_error")
        print(error)

    # run when websocket is closed
    def on_close(self, _):
        print("### closed ###")

    # run when websocket is initialised
    def on_open(self, _):
        print(f'Connected to {self.exchange}\n')




