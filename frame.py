#!/usr/bin/env python3

from pprint import pprint

ASK = "asks"
BID = "bids"
DEFAULT_DEPTH = 10


class OrderBook(object):
    
    def __init__(self, pair):
        self.pair = pair
        self.asks = {}
        self.bids = {}
        self.book = dict(name=self.name,
                         pair=self.pair,
                         asks=self.asks,
                         bids=self.bids)
        
    def __repr__(self):
        return "%s(pair=%s, asks=%s, bids=%s)" \
            % (self.name,
               self.pair,
               self.asks,
               self.bids)
        
    @property
    def name(self):
        return self.__class__.__name__
    
    def reverse(self, side):
        return False if side == ASK else True
    
    def remove(self, side, price):
        del self.book[side][price]
    
    def update(self, side, price, amount):
        self.book[side][price] = amount

    def insert(self, side, price, amount):
        self.book[side][price] = amount
        self.maintain_depth(side)
    
    def sort_book(self, book, reverse, depth=DEFAULT_DEPTH):
        return sorted(book.items(), reverse=reverse)[:depth]
    
    def maintain_depth(self, side):
        if side == ASK:
            self.asks = dict(self.sort_book(book=self.asks,
                                            reverse=self.reverse(side)))
        if side == BID:
            self.bids = dict(self.sort_book(book=self.bids,
                                       reverse=self.reverse(side)))
    
    # def maintain_depth(self, book, side, reverse, depth=DEFAULT_DEPTH):
    #     self.maintain_depth(side)

    # def dict_sort_slice(self, *, book, reverse, depth=DEFAULT_DEPTH):
    #     result = sorted(book.items(), reverse=reverse)[:depth]
    #     self.book[side].update(result)
    #     return dict(sorted(book.items(), reverse=reverse)[:depth])
    
    # def maintain_depth(self, side):
    #     self.book[side] = self.dict_sort_slice(book = self.book[side],
    #                                            reverse = self.reverse(side))


o = OrderBook("BTC/USD")
o.update(side=ASK, price='7201', amount="1")
o.update(side=ASK, price='7202', amount='2')
o.update(side=ASK, price='7203', amount='3')
o.update(side=ASK, price='7204', amount='4')
o.update(side=ASK, price='7205', amount='5')
o.update(side=ASK, price='7206', amount='6')
o.update(side=ASK, price='7207', amount='7')

o.insert(side=ASK, price='7204.6', amount='8')
print(o)

# ret = sorted(o.asks.items(), reverse=False)[:5]
# o.asks = dict(ret)
# print(o)