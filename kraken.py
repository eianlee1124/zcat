#!/usr/bin/env python3

from table import Table
from websocketapi import WebSocketAPI

class Kraken(object):
    
    def __init__(self, pair, url, payload):
        self.pair = pair
        self.url = url
        self.payload = payload
        self.payload['pair'].append(pair)
        
        self.table = Table()
        self.ws = WebSocketAPI()
    
            
    


if __name__ == "__main__":
    from config import KrakenConfig as kconfig
    pair = "BTC/USD"
    url = kconfig.url
    payload = kconfig.payload
    k = Kraken(pair, url, payload)
    k.ws.connect(url)
    k.ws.send(payload)
    
    while k.ws.connected:
        print(k.ws.recv())