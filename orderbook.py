#!/usr/bin/env python3


# Built-in
import ssl
import json
import pprint
import datetime
import itertools

# Third-party
import websocket


# Home-Brew
from defines import sslopt

ASK = "asks"
BID = "bids"
DEFAULT_DEPTH = 10


class Order:
    
    def __init__(self, uid, side, price, amount):
        self._uid = uid
        self._side = side
        self._price = price
        self._amount = amount
        
    def __repr__(self):
        return "%s(tid=%s, side=%s, price=%s, amount=%s)" % (self.__class__.__name__,
                                                             self.uid,
                                                             self.side,
                                                             self.price,
                                                             self.amount)
    @property
    def uid(self):
        return self._uid

    @property
    def side(self):
        return self._side

    @property
    def price(self):
        return self._price

    @property
    def amount(self):
        return self._amount


class OrderBook:
    
    def __init__(self, pair):
        self.pair = pair
        self.asks = {}
        self.bids = {}
        self.book = dict(name=self.name,
                         pair=self.pair,
                         asks=self.asks,
                         bids=self.bids)
    
    @property
    def name(self):
        return self.__class__.__name__
    
    def reverse(self, side):
        return False if side == ASK else True
    
    def remove(self, side, price):
        """오더북 특정 레벨의 주문을 삭제."""
        del self.book[side][price]
        
    def update(self, book, side, price, amount):
        """오더북 특정 레벨의 주문을 갱신."""
        self.book[side].update({price: amount})

    def insert(self, book, side, price, amount):
        """오더북에 새로운 주문을 삽입한 뒤, 
        정렬 후 슬라이싱하여 오더북의 깊이를 유지한다."""
        
        self.book[side][price] = amount
        self.maintain_depth(side)
    
    def book_sort(self, *, book, reverse):
        return sorted(book.items(), reverse=reverse)
    
    def book_slice(self, *, book, reverse, depth=DEFAULT_DEPTH):
        return dict(itertools.islice(self.book_sort(book=book, reverse=reverse), depth))
    
    def maintain_depth(self, side):
        self.book[side] = self.book_slice(book=self.book[side], reverse=self.reverse(side))



class WebSocketAPI(OrderBook):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ws = websocket.WebSocket(sslopt=sslopt)
    
    @property
    def connected(self):
        return self.ws.connected

    def connect(self, url):
        """주어진 url에 웹소켓 연결을 만든다.
        """
        self.ws.connect(url)
        
    def send(self, payload):
        """주어진 payload를 연결 대상으로 전송.
        """
        payload = json.dumps(payload)
        self.ws.send(payload)
        
    def recv(self):
        """메시지 수신 이벤트가 발생하면 json으로 포맷팅 후 반환.
        """
        return json.loads(self.ws.recv())
    
    
            
# if __name__ == "__main__":
#     from base.config import KrakenConfig as config
    
#     pair = "BTC/USD"
#     url = config.url
#     payload = config.payload
#     payload['pair'] = [pair]
    
#     kraken = Kraken(pair=pair, url=url, payload=payload)
#     kraken.connect(url)
#     kraken.send(payload)
    
#     while kraken.is_connected:
#         kraken.receiver()
    
    