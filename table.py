#!/usr/bin/env python3

from datetime import datetime

ASK = "asks"
BID = "bids"
DEFAULT_DEPTH = 5

class Table(object):
    """오더북 삽입, 갱신, 삭제를 위한 베이스 클래스.
    """
    
    def __init__(self):
        self.book = {ASK: {}, BID: {}}
        
    def __repr__(self):
        return "%s(asks=%s, bids=%s, updates=%s)" % \
            (self.name,
             self.book[ASK],
             self.book[BID],
             self.nonce)
    
    @property
    def name(self):
        return self.__class__.__name__
    
    @property
    def nonce(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    def reverse(self, side):
        """주어진 주문타입에 따라 정렬 시 필요한 불린값 반환
        """
        return False if side == ASK else True
        
    def remove(self, side, price):
        """특정 레벨의 주문을 삭제
        """
        del self.book[side][price]

    def update(self, side, price, amount):
        """특정 레벨의 주문을 갱신
        """
        self.book[side][price] = amount

    def insert(self, side, price, amount):
        """특정 레벨에 새로운 주문을 삽입
        """
        self.book[side][price] = amount
        self.maintain_depth(side)

    def sort_book(self, book, reverse, depth=DEFAULT_DEPTH):
        """오더북을 정렬 후 슬라이싱하여 딕셔너리로 반환
        """
        return dict(sorted(book.items(), reverse=reverse)[:depth])
    
    def maintain_depth(self, side):
        """inplace 정렬 및 슬라이싱
        """
        self.book[side] = self.sort_book(self.book[side], self.reverse(side))
        


if __name__ == "__main__":
    t = Table()
    
    prices = [str(price) for price in reversed(range(7201, 7211))]
    amounts = [str(amount) for amount in range(1, len(prices)+1)]
    
    orders = zip(prices, amounts)
    
    for price, amount in orders:
        t.update(side=ASK,
                 price=price,
                 amount=amount)
        
    t.insert(side=ASK, price="7203.5", amount="insert")
    
    print("=" * 100)
    print(t)