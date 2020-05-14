import asyncio
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
    
