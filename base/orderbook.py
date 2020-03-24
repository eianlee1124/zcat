#!/usr/bin/env python3


import operator
import _collections

ASK = "asks"
BID = "bids"
DEPTH = 10

def is_reverse(side):
    return side == "bids"

class OrderBook(object):
    
    __slots__ = ("side", "data")
    
    def __init__(self, side):
        self.side = side
        self.data = {}
        
    def __repr__(self):
        return "%s" % self.data
    
    def process(self, price, amount, is_snapshot=False):
        if is_snapshot:
            self.update(price, amount)
        elif price in self.data:
            if float(amount) == 0:
                self.remove(price)
            if float(amount) != 0:
                self.update(price, amount)
        elif price not in self.data and float(amount) != 0:
            self.insert(price, amount)

    def remove(self, price):
        del self.data[str(price)]
        
    def update(self, price, amount):
        self.data[str(price)] = amount

    def insert(self, price, amount):
        self.update(price, amount)
        self.sort(self.side)
        
    def sort(self, side, key=operator.itemgetter(0), reverse=is_reverse):
        self.data = dict(sorted(self.data.items(), key=key, reverse=reverse(self.side))[:DEPTH])
        
        