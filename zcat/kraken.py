#!/usr/bin/env python3

import asyncio
import ujson as json

from config import KRAKEN as config
from defines import ASK, BID
from orderbook import Amount, Price
from websocketapi import WebSocketAPI


class Kraken(WebSocketAPI):
    
    def __init__(self, pair, url=None, payload=None):
        self.pair = pair
        self.url = url or config.URL
        self.payload = payload or config.PAYLOAD
        self.payload['pair'].append(pair)
        super().__init__(self.pair, self.url, self.payload)
        
    def __repr__(self):
        return "%s(...)\n" % (self.__class__.__name__)

        
    async def message_handler(self, message):
        message = json.loads(message)
        for msg in message:
            if isinstance(msg, dict):
                for key, updates in msg.items():
                    for update in updates:
                        price, amount = Price(update[0]), Amount(update[1])
                        side = BID if key.startswith('b') else ASK
                        self.l2_book.process(side, price, amount) # 크라켄은 스냅샷부터 모든 메시지를 l2_book.process로 처리한다.
        print(self)
                
