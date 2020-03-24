#!/usr/bin/env python3


import ssl
import pprint
import threading

import ujson as json
from websocket import WebSocket
from orderbook import OrderBook


class Bitstamp(object):
    
    def __init__(self, pair, sslopt={"cert_reqs": ssl.CERT_NONE}):
        self.pair = pair
        self.asks = OrderBook("asks")
        self.bids = OrderBook("bids")
        self.ws = WebSocket(sslopt=sslopt)
        
    def subscribe(self):
        self.ws.connect("wss://ws.bitstamp.net")
        self.ws.send(json.dumps({
            "event": "bts:subscribe",
            "data": {
                "channel": "order_book_btcusd"
            },
        }))
        
        while self.ws.connected:
            message = json.loads(self.ws.recv())
            pprint.pprint(message)
            
    def run(self):
        t = threading.Thread(target=self.subscribe)
        t.start()
        
if __name__ == "__main__":
    b = Bitstamp("BTC/USD")
    b.run()