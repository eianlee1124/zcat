#!/usr/bin/env python3


import asyncio

from exchanges import *


_EXCHANGES = dict(
    Bitfinex = Bitfinex,
    Kraken = Kraken
)

class Exchange:
    
    def __init__(self, retries=10, timeout_interval=10):
        self.feeds = []
        self.retries = retries
        self.timeout = {}
        self.last_msg = {}
        self.timeout_interval = timeout_interval
        
    def add_feed(self, feed, timeout=120, **kwargs):
        if isinstance(feed, str):
            if feed in _EXCHANGES:
                self.feeds.append(_EXCHANGES[feed](**kwargs))
                feed = self.feeds[-1]
                self.last_msg[feed.uuid] = None
                self.timeout[feed.uuid] = timeout
            else:
                raise ValueError("지원하지 않는 거래소: %s" % feed)
        