#!/usr/bin/env python3

import json
from pprint import pformat
from datetime import datetime

from sortedcontainers.sorteddict import SortedDict

from defines import ASK, BID, DEFAULT_DEPTH
from utils import generate_asks, generate_bids, timing


class Price(float):
    """Price field object. inherite from `float`
    """
    __slots__ = ('value')
    
    def __init__(self, value=0.0):
        if isinstance(value, (int, str)):
            value = float(value)
        self.value = value

    def __repr__(self):
        return "%s(%.8f)" % (self.__class__.__name__, self.value)
        
    def __neg__(self):
        return Price(-self.value)
    
    def __abs__(self):
        return Price(abs(self.value))
    
    
class Amount(float):
    """Amount field object. inherite from `float`
    """
    __slots__ = ('value')

    def __init__(self, value=0.0):
        if isinstance(value, (int, str)):
            value = float(value)
        self.value = value

    def __repr__(self):
        return "%s(%.8f)" % (self.__class__.__name__, self.value)
    
    def __neg__(self):
        return Amount(-self.value)
    
    def __abs__(self):
        return Amount(abs(self.value))


class Order(object):
    """정렬된 상태를 유지하며 주문 로직을 처리하기 위한 클래스.
    """
    
    __slots__ = ('side', 'store', 'order', 'prices', 'quotes')
    
    def __init__(self, side: str):
        self.side = side
        self.store = set()
        self.order = SortedDict()
        self.prices = self.order.keys()     # dtype -> SortedKeysView
        self.quotes = self.order.items()    # dtype -> SortedItemsView
        
    def __repr__(self):
        return "%s: %s\n" % (self.side, self.order)
    # def __str__(self):
    #     return "%s: %s" % (self.side, self.order)
        
    def __contains__(self, price):
        """Runtime complexity: `O(1)`
        """
        return price in self.store
        
    def __len__(self):
        return len(self.quotes)
    
    @property
    def worst_offer(self):
        """각 주문타입에 따라 스프레드에서 가장 먼 가격을 반환한다.
        
        - ASK: 인덱스의 마지막 가격을 반환
        - BID: 인덱스의 처음 가격을 반환
        """ 
        return self.quotes[0 if self.side == BID else -1][0]
    
    
    def update(self, price, amount):
        """아래 조건 충족 시 기존의 주문을 갱신.
        
        - 업데이트 이벤트 (거래소마다 상이)
        - `price`가 in-memoery 오더북의 멤버인 경우
        """
        self.order[price] = amount
        self.store.add(price)
    
    
    def insert(self, price, amount):
        """아래 조건 충족 시 새로운 주문을 삽입 후 슬라이싱.
        
        - 삽입 이벤트 (거래소마다 상이)
        - `price`가 인-메모리 오더북의 멤버가 아닌 경우
        """
        def islice(depth=DEFAULT_DEPTH):
            while len(self.quotes) > depth: 
                self.discard(self.worst_offer)
                
        self.order[price] = amount
        self.store.add(price)
        islice(DEFAULT_DEPTH)

    def discard(self, price):
        """아래 조건 충족시 기존의 주문을 삭제.
        
        - 삭제 이벤트 (거래소마다 상이함)
        - `price`가 오더북의 멤버인 경우
        """
        try:
            del self.order[price]
            self.store.discard(price)
        except KeyError:
            pass
    
    
    def process(self, side, price, amount):
        """인-메모리 오더북 업데이트, 추가, 제거 프로세스.
        
        self.order의 멤버쉽 연산 runtime complexity: `O(log N)`
        
        self.store의 멤버쉽 연산 runtime complexity: `O(1)`
        """
        def is_updatable(new_price):
            """
            - ASK의 경우 새로운 가격이 최대가격 보다 작은 경우 
                - i.g. new_price < old_price
                
            - BID의 경우 최소가격이 새로운 가격보다 작은 경우
                - i.g. old_price < new_price
            """
            if len(self) < DEFAULT_DEPTH:
                return True

            old_price = self.worst_offer
            return old_price < new_price if self.side == BID else new_price < old_price
        
        assert side == self.side    # 잘못된 매수 또는 매도주문을 처리하려는 경우

        if amount == 0:
            self.discard(price)
        elif price in self.store: 
            self.update(price, amount)
        elif is_updatable(price):
            self.insert(price, amount)

            
            

class OrderBook(dict):
    """정렬된 상태를 유지하며 주문 정보를 담는 mutable mapping 클래스.
    
    - builtin class `dict`로 부터 상속받음.
    - `__slots__`을 사용하여 `__dict__`를 생성하지 않음.
    """
    
    __slots__ = ('asks', 'bids')
    
    def __init__(self, pair):
        self.asks = Order(ASK)
        self.bids = Order(BID)
        super().__init__({pair: {ASK: self.asks, BID: self.bids}})
    
    def __repr__(self):
        return "%s\n%s\n" % (self.bids, self.asks)
    # def __str__(self):
    #     return "%s: %s" % (self.bids, self.asks)
    
    
    def update(self, side, price, amount):
        """매수, 매도에 관계없이 인-메모리 오더북의 주문을 갱신한다.
        """
        order = self.bids if side == BID else self.asks
        order.update(price, amount)
        
    def insert(self, side, price, amount):
        """매수, 매도에 관계없이 인-메모리 오더북의 주문을 삽입한다.
        """
        order = self.bids if side == BID else self.asks
        order.insert(price, amount)
        
    def discard(self, side, price):
        """매수, 매도에 관계없이 인-메모리 오더북의 주문을 삭제한다.
        """
        order = self.bids if side == BID else self.asks
        order.discard(price)
    
    def process(self, side, price, amount):
        """매수, 매도에 관계없이 삽입, 갱신, 삭제 로직을 처리한다.
        """
        order = self.bids if side == BID else self.asks
        order.process(side, price, amount)
