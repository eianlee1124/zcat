#!/usr/bin/env python3


import ssl
import threading

import ujson as json
from websocket import WebSocket
from orderbook import OrderBook


class Kraken(object):
    
    def __init__(self, pair, sslopt={"cert_reqs": ssl.CERT_NONE}):
        self.pair = pair
        self.asks = OrderBook("asks")
        self.bids = OrderBook("bids")
        self.ws = WebSocket(sslopt=sslopt)
        
    def subscribe(self):
        self.ws.connect("wss://ws.kraken.com")
        self.ws.send(json.dumps({
            "event": "subscribe",
            "pair": [self.pair],
            "subscription": {
                "name": "book"
            }
        }))
        
        while self.ws.connected:
            message = json.loads(self.ws.recv())
            for msg in message:
                if type(msg) is dict:
                    for key, orders in msg.items():
                        for price, amount, *_ in orders:
                            if key == "as":
                                self.asks.process(price, amount, is_snapshot=True)
                            elif key == "bs":
                                self.bids.process(price, amount, is_snapshot=True)
                            elif key == "a":
                                self.asks.process(price, amount)
                            elif key == "b":
                                self.bids.process(price, amount)
            with open("asks.txt", "w") as f:
                f.write(json.dumps(self.asks.data, indent=4))
            with open("bids.txt", "w") as f:
                f.write(json.dumps(self.bids.data, indent=4))
                                
    def run(self):
        t = threading.Thread(target=self.subscribe)
        t.start()