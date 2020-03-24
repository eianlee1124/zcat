#!/usr/bin/env python3


import ssl
import json
import threading

from websocket import WebSocket
from orderbook import OrderBook


class Bitfinex(object):
    
    def __init__(self, pair, sslopt={"cert_reqs": ssl.CERT_NONE}):
        self.pair = pair
        self.asks = OrderBook("asks")
        self.bids = OrderBook("bids")
        self.ws = WebSocket(sslopt=sslopt)
        
    def subscribe(self):
        base, quote = self.pair.split('/')
        self.ws.connect("wss://api-pub.bitfinex.com/ws/2")
        self.ws.send(json.dumps({
            "event": "subscribe",
            "channel": "book",
            "symbol": f"t{base}{quote}"
        }))
        
        while self.ws.connected:
            message = json.loads(self.ws.recv())
            for msg in message:
                if type(msg) is list:
                    if len(msg) == 50:
                        for price, _, amount in msg:
                            if amount < 0:
                                self.asks.process(price, amount, is_snapshot=True)
                            if amount > 0:
                                self.bids.process(price, amount, is_snapshot=True)
                    if len(msg) == 3:
                        price, count, amount = msg
                        if count > 0:
                            if amount < 0:
                                self.asks.process(price, amount)
                            if amount > 0:
                                self.bids.process(price, amount)
                        if count == 0:
                            if amount == -1:
                                self.asks.process(price, 0)
                            if amount == 1:
                                self.bids.process(price, 0)
                                
            with open("asks.txt", "w") as f:
                f.write(json.dumps(self.asks.data, indent=4))
            with open("bids.txt", "w") as f:
                f.write(json.dumps(self.bids.data, indent=4))
                                
    def run(self):
        t = threading.Thread(target=self.subscribe)
        t.start()
        
        
if __name__ == "__main__":
    b = Bitfinex("BTC/USD")
    b.run()