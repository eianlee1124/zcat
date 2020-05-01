import asyncio
from kraken import Kraken
from bitfinex import Bitfinex


_EXCHANGES = {
    'Kraken': Kraken,
    'Bitfinex': Bitfinex
}

pair = 'BTC/USD'
feeds = [exchange(pair) for exchange in [Kraken, Bitfinex]]

try:
    loop = asyncio.get_event_loop()
    for feed in feeds:
        loop.create_task(feed.)
        