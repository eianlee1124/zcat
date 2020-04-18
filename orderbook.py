#!/usr/bin/env python3

import logging
from _collections_abc import Set
from functools import wraps

from sortedcontainers.sorteddict import SortedDict, SortedSet

from utils import generate_asks, generate_bids
from defines import ASK, BID, DEFAULT_DEPTH

logging.basicConfig(
  format = '%(asctime)s: %(levelname)s: %(message)s',
  datefmt = '[%Y-%d-%m  %I:%M:%S]',
  level = logging.INFO
)

logger = logging.getLogger(__name__)

def log_decorator(func):
    """Flow control 확인용 logger decorator 함수."""
    logger = logging.getLogger(__name__)
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info("<%s> %s %s" % (
                func.__name__.capitalize(),
                args[0], args[1]
            ))
            func(*args, **kwargs)
        except Exception as e:
            logger.debug("Exception {}".format(e))
            raise e
    return wrapper


class OrderBook(object):
    """정렬된 상태를 유지하는 OrderBook 클래스.
    """
    
    __slots__ = ('side', 'store', 'order', 'prices', 'quotes')
    
    def __init__(self, side: str):
        self.side = side
        self.store = set()
        self.order = SortedDict()
        self.prices = self.order.keys()
        self.quotes = self.order.items()
        
    def __contains__(self, price):
        return price in self.store
        
    def __len__(self):
        return len(self.quotes)
        
    def __repr__(self):
        ret = ''
        for price, amount in self.quotes:
            ret += '%s(Price(%s): Amount(%s))\n' % (
                self.side, price, amount
            )
        return ret
    
    @staticmethod
    def logger(func, *args):
        logger.info('\r<%s.%s> Price(%s): Amount(%s)' % (
            func.__self__.side.capitalize(),
            func.__name__.capitalize(),
            args[0], args[1]
        ))
    
    @property
    def worst_offer(self):
        """각 주문타입에 따라 스프레드에서 가장 먼 가격을 반환한다.
        
        - ASK의 경우 인덱스 마지막 가격을 반환
        - BID의 경우 인덱스의 처음 가격을 반환
        """ 
        return self.quotes[0 if self.side == BID else -1][0]
    
    def update(self, price, amount):
        """기존의 주문을 갱신한다.
        
        - 수량이 0이 아닌경우
        - `price`가 오더북의 멤버인 경우
        """
        self.order[price] = amount
        self.store.add(price)
    
    def insert(self, price, amount):
        """새로운 주문을 삽입한다.
        
        - 수량이 0이 아닌경우
        - `price`가 오더북의 멤버가 아닌 경우
        """
        def islice(depth=10):
            while len(self.quotes) > depth: 
                self.discard(self.worst_offer)
                
        self.order[price] = amount
        self.store.add(price)
        islice(10)

    def discard(self, price):
        """기존의 주문을 삭제한다.
        
        - 수량이 0인 경우
        - `price`가 오더북의 멤버인 경우
        """
        try:
            del self.order[price]
            self.store.discard(price)
        except KeyError:
            pass
    
    
    def process(self, side, price, amount, debug=False):
        """업데이트 로직
        - ASK의 경우 새로운 가격이 최대가격보다 작아야 업데이트 i.g.  new_price <= ask_max_price
        - BID의 경우 새로운 가격이 최소가격보다 커야 업데이트 i.g. bid_min_price <= new_price
        """
        def is_updatable(new_price):
            """
            - new_price < ask_max_price
            - bid_min_price < new_price 
            """
            if len(self) < DEFAULT_DEPTH:
                return True

            old_price = self.worst_offer
            return old_price < new_price if self.side == BID else new_price <  old_price
        
        assert side == self.side    # 잘못된 매수 또는 매도주문을 처리하려는 경우
        if amount == 0:
            self.remove(price)
        elif price in self.store:
            self.update(price, amount)
        elif is_updatable(price):
            self.insert(price, amount)
            
        if debug:
            print(self)
                
if __name__ == "__main__":
    print("=" * 40 + "테스트 시작" + "=" * 40)
    asks = OrderBook(ASK)
    bids = OrderBook(BID)
    
    generate_asks(asks, start=7200, depth=10, debug=False)
    generate_bids(bids, start=7200, depth=10, debug=False)
    assert len(asks) == DEFAULT_DEPTH  # islice 테스트
    assert len(bids) == DEFAULT_DEPTH  # islice 테스트
    
    asks.process(ASK, 7200, 1000, debug=False)   # update 테스트
    bids.process(BID, 7199, 1000, debug=False)   # update 테스트 
    assert 7200 in asks # min price 테스트
    assert 7209 in asks and 7209 == asks.worst_offer # max price 테스트     
    
    assert 7199 in bids # max price 테스트
    assert 7190 in bids and 7190 == bids.worst_offer # min price 테스트

    print("=" * 40 + "테스트 종료" + "=" * 40)
    