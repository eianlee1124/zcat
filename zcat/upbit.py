#!/usr/bin/env python3


import uuid

import ujson as json

from config import UPBIT as config
from defines import ASK, BID
from orderbook import Amount, Price
from websocketapi import WebSocketAPI


class Upbit(WebSocketAPI):
    
    def __init__(self, pair, url, payload):
        base, quote = pair.split('/')
        self.pair = "{}-{}".format(quote, base)
        self.url = url
        self.payload = payload
        self.payload[0]['ticket'] = 'UPBIT' + str(uuid.uuid4())
        self.payload[1]['codes'].append(self.pair)
        super().__init__(self.pair, self.url, self.payload)
        
    async def message_handler(self, message):
        message = json.loads(message)
        # 업비트가 스냅샷을 보내주는 의미가 있는지 모르겠음
        for msg in message['obu']:
            asks = ASK, Price(msg['ap']), Amount(msg['as'])
            bids = BID, Price(msg['bp']), Amount(msg['bs'])
            self.l2_book.insert(*asks)
            self.l2_book.insert(*bids)
            
            
if __name__ == "__main__":
    upbit = Upbit('BTC/KRW', config.URL, config.PAYLOAD)
    upbit.run()