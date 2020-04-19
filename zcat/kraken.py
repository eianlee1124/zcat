#!/usr/bin/env python3


import ujson as json

from config import KRAKEN as config
from defines import ASK, BID
from orderbook import Amount, Price
from websocketapi import WebSocketAPI


class Kraken(WebSocketAPI):
    
    def __init__(self, pair, url, payload):
        self.pair = pair
        self.url = url
        self.payload = payload
        self.payload['pair'].append(pair)
        super().__init__(self.pair, self.url, self.payload)
        
    async def message_handler(self, message):
        message = json.loads(message)
        for msg in message:
            if isinstance(msg, dict):
                for key, updates in msg.items():
                    for update in updates:
                        price, amount = Price(update[0]), Amount(update[1])
                        side = BID if key.startswith('b') else ASK
                        self.l2_book.process(side, price, amount) # 크라켄은 그냥 l2_book.process로 처리한다.
                        

if __name__ == "__main__":
    kraken = Kraken("BTC/USD", config.URL, config.PAYLOAD)
    kraken.run()
