#!/usr/bin/env python3


import logging
from decimal import Decimal
from time import perf_counter
from functools import wraps


logging.basicConfig(
  format = '%(asctime)s: %(levelname)s: %(message)s',
  datefmt = '[%Y-%d-%m  %I:%M:%S]',
  level = logging.INFO
)

logger = logging.getLogger(__name__)

def generate_asks(order, start=7200, depth=15, debug=False):
    """매수 주문을 오름차순으로 생성한다.
    """
    price = start
    for n in range(1, depth+1):
        order.process('asks', price+n, n, debug)
    
def generate_bids(order, start=7200, depth=15, debug=False):
    """매도 주문을 내림차순으로 생성한다.
    """
    price = start
    for n in range(1, depth+1):
        order.process('bids', price-n, n, debug)
        
        
def timing(func):
    """작동시간 측정 데코레이터용 함수
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        ret = func(*args, **kwargs)
        end = perf_counter()
        elapsed = Decimal(end - start)
        logger.info("\rElapsed time: %s, name(%s), args(%s), kwargs(%s)" % (
            elapsed, func.__name__, args, kwargs
        ))
        return ret
    return wrapper
        