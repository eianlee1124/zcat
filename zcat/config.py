from defines import DEFAULT_DEPTH

class KRAKEN:
    URL = "wss://ws.kraken.com"
    PAYLOAD = {"event": "subscribe",
               "pair": [],
               "subscription": {
                   "name": "book",
                   "depth": DEFAULT_DEPTH
               }}
    
class BITFINEX:
    URL = "wss://api-pub.bitfinex.com/ws/2"
    PAYLOAD = {'event': 'subscribe',
               'channel': 'book',
               'symbol': '',
               'freq': 'F0',
               'len': '25'}
    

class UPBIT:
    URL = "wss://api.upbit.com/websocket/v1"
    PAYLOAD = [
        {"ticket": ""},
        {"type": "orderbook", "codes": []},
        {"format": "SIMPLE"}
    ]