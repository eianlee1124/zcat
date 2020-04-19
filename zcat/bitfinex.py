#!/usr/bin/env python3

from decimal import Decimal
from operator import neg
import ujson as json

from config import BITFINEX as config
from defines import ASK, BID, DEFAULT_DEPTH
from orderbook import Amount, Price
from websocketapi import WebSocketAPI



class Bitfinex(WebSocketAPI):
    
    def __init__(self, pair, url, payload):
        self.pair = "t{}{}".format(*pair.split('/'))
        self.url = url
        self.payload = payload
        self.payload['symbol'] = self.pair
        super().__init__(self.pair, self.url, self.payload)
        
    async def message_handler(self, message):
        """Bitfinex message handler.
        
        1. subscribe to channel
        2. receive the book snapshot and create your in-memory book structure.
        3. when count > 0 then add or update the price level.
          - 3.1 if amount > 0 then add/update bids
          - 3.2 if amount < 0 then add/update asks
        4. when count = 0 then delete the price level.
          - 4.1 if amount == 1 then remove from bids.
          - 4.2 if amount == -1 then remove from asks.

        """
        message = json.loads(message)
        if isinstance(message, list):
            if isinstance(message[1][0], list):
                # snapshot
                for msg in message[1]:
                    price, amount = Price(msg[0]), Amount(msg[2])
                    if amount > 0:
                        side = BID
                    else:
                        side = ASK
                        amount = abs(amount)
                    self.l2_book.process(side, price, amount)
            elif message[1] != 'hb':
                # orderbook update
                price, count, amount = Price(message[1][0]), message[1][1], Amount(message[1][2])
                
                if amount > 0:
                    side = BID
                else:
                    side = ASK
                    amount = abs(amount)
                    
                if count > 0:
                    # add or update
                    self.l2_book.process(side, price, amount)
                else:
                    # remove
                    self.l2_book.discard(side, price)

    
if __name__ == "__main__":
    bitfinex = Bitfinex("BTC/USD", config.URL, config.PAYLOAD)
    bitfinex.run()