#!/usr/bin/env python3


import abc
import asyncio
import json
import sys
from pprint import pprint

import websockets

from defines import ASK, BID
from orderbook import OrderBook

write = sys.stdout.write
flush = sys.stdout.flush

class WebSocketAPI(object):
    
    def __init__(self, pair, url, payload):
        self.url = url
        self.payload = payload
        self.pair = pair
        self.l2_book = OrderBook(self.pair)
        
    async def connect(self):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(json.dumps(self.payload))
            
            while True:
                # 비동기가 아닌 경우 수신된 메시지가 없을 때 sleep을 해줘야 GIL이 해제되지만,
                # await 키워드를 사용하는 경우는 어떻게 되는 건지?
                message = await websocket.recv()
                await self.message_handler(message)
                
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())
        
    @abc.abstractmethod
    async def message_handler(self, message):
        '웹소켓 메시지 핸들러'
