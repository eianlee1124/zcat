#!/usr/bin/env python3


import abc
import asyncio
import time
import json
import sys
from socket import error as socket_error
from pprint import pprint, pformat

import websockets
from websockets import ConnectionClosed

from logger import get_logger
from defines import ASK, BID
from orderbook import OrderBook

LOG = get_logger('WebSocketAPI', 'wss.log')

write = sys.stdout.write
flush = sys.stdout.flush

class WebSocketAPI(object):
    stores = {}
    
    def __init__(self, pair, url, payload):
        self.url = url
        self.payload = payload
        self.pair = pair
        self.l2_book = OrderBook(pair)
        
    def __repr__(self):
        return pformat(self.stores)
        
    @property
    def name(self):
        return self.__class__.__name__
        
    async def connect(self):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(json.dumps(self.payload))
            
            while True:
                # 비동기가 아닌 경우 수신된 메시지가 없을 때 sleep을 해줘야 GIL이 해제되지만,
                # await 키워드를 사용하는 경우는 어떻게 되는 건지?
                message = await websocket.recv()
                await self.message_handler(message)
                await self.book_callback()
        
    async def book_callback(self):
        name = self.name
        book = self.l2_book
        self.stores.update({name: book})
        print(self)
        
    @abc.abstractmethod
    async def message_handler(self, message):
        '웹소켓 메시지 핸들러'
