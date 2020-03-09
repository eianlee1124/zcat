class KrakenConfig(object):
    url = "wss://ws.kraken.com"
    payload = {
        'event': 'subscribe',
        'pair': [],
        'subscription': {
            'name': 'book'
        },
    }


class BitfinexConfig:
    url = "wss://api-pub.bitfinex.com/ws/2"
    payload = {
        'event': 'subscribe',
        'channel': 'book',
        'symbol': 't{}{}',
        'prec': 'P0',
        'freq': 'F0',
        'len': 25
    }
    
    
class UpbitConfig:
    url = "wss://api.upbit.com/websocket/v1"
    payload = [{"ticket":"test"},
               {"type":"orderbook","codes":["{}-{}"]}]