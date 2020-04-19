class KRAKEN:
    URL = "wss://ws.kraken.com"
    PAYLOAD = {"event": "subscribe",
               "pair": [],
               "subscription": {"name": "book"}}
    
class BITFINEX:
    URL = "wss://api-pub.bitfinex.com/ws/2"
    PAYLOAD = {'event': 'subscribe',
               'channel': 'book',
               'symbol': '',
               'freq': 'F0',
               'len': '25'}
    
    
