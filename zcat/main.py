import asyncio
from threading import Thread
from kraken import Kraken
from bitfinex import Bitfinex

def main(pair='BTC/USD'):
    feeds = []
    for exchange in [Kraken, Bitfinex]:
        feeds.append(exchange(pair))
    try:
        loop = asyncio.get_event_loop()
        for feed in feeds:
            loop.create_task(feed.connect())
        loop.run_forever()
    except Exception as e:
        asyncio.sleep(1)
        
if __name__ == "__main__":
    main()

# def coro1(pair):
#     kraken = Kraken(pair)
#     yield from kraken.connect()
    
# def coro2(pair):
#     bitfinex = Bitfinex(pair)
#     yield from bitfinex.connect()

# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()
#     loop.create_task([coro1('BTC/USD'), coro2('BTC/USD')])
#     loop.run_forever()