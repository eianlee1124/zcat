#!/usr/bin/env python3


import abc
import asyncio
import json

import websockets

from defines import ASK, BID
from orderbook import Amount, OrderBook, Price


class WebSocketAPI(object):
    
    def __init__(self, pair, url, payload):
        self.url = url
        self.payload = payload
        self.pair = pair
        self.l2_book = OrderBook()
        
    async def connect(self):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(json.dumps(self.payload))
            
            while True:
                # 비동기가 아닌 경우 수신된 메시지가 없을 때 sleep을 해줘야 하는데,
                # await 키워드를 사용하면 안해줘도 되는건지?
                message = await websocket.recv()
                await self.message_handler(message)
                print(self.l2_book)
                

        
    def run(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect())
        
    @abc.abstractmethod
    async def message_handler(self, message):
        '웹소켓 메시지 핸들러'
