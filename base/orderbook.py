#!/usr/bin/env python3

import ssl
import json
import operator
import collections
import websocket


ASK = "asks"
BID = "bids"
DEPTH = 10
SSLOPT = {"cert_reqs": ssl.CERT_NONE}


class Order(collections.OrderedDict):
    pass


class OrderBook(object):

    def __init__(self, side):
        self.side = side
        self.data = Order()
        self.text = json.dumps(self.data.__dict__, indent=4)
       
    def __repr__(self):
        return "%s" % self.data

    def __contains__(self, key):
        try:
            self.data[str(key)]
            return True
        except KeyError:
            return False

    def process(self, price, amount, is_snapshot=False):
        if is_snapshot:
            self.update(price, amount)
        elif price in self.data:
            if float(amount) == 0:
                self.remove(price)
            if float(amount) != 0:
                self.update(price, amount)
        elif price not in self.data:
            self.insert(price, amount)

    def remove(self, price):
        del self.data[price]

    def update(self, price, amount):
        self.data[str(price)] = amount

    def insert(self, price, amount):
        self.update(price, amount)
        self.sort(self.side)

    def sort(self, side, key=operator.itemgetter(0), reverse=is_reverse):
        self.data = Order(sorted(self.data.items(),
                                 key=key,
                                 reverse=reverse(self.side))[:DEPTH])


class Exchange(object):

    URL = "NotImplemented"
    PAYLOAD = {}

    def __init__(self):
        self.ws = websocket.WebSocket(sslopt=SSLOPT)
    
    def connect(self, url):
        self.ws.connect(url)

    def send(self, payload):
        self.ws.send(json.dumps(payload))

    def recv(self):
        return json.loads(self.ws.recv())

    def handler(self, url, payload):
        return NotImplemented
