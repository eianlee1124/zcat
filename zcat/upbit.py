#!/usr/bin/env python3


import ujson as json

from config import KRAKEN as config
from defines import ASK, BID
from field import Amount, Price
from websocketapi import WebSocketAPI


class Upbit(WebSocketAPI):
    
    def __init__(self, pair, url, payload):
        base, quote = pair.split('/')
        self.pair = "{}-{}".format(quote, base)
        self.url = url
        self.payload = payload
        super().__init__(self.pair, self.url, self.payload)
        
    async def message_handler(self, message):
        message = json.loads(message)
        print(message)