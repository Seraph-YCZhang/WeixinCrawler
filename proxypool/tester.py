import aiohttp
import asyncio
import time
from db import RedisClient

VALID_STATUS_CODE = [200]
TEST_URL = "www.baidu.com"
BATCH_TEST_SIZE = 100

class Tester():
    def __init__(self):
        self.redis = RedisClient()
    
    async def single_test(self, proxy):
        # try connecting with single proxy
        conn = aiohttp.TCPConnector(ssl = False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                real_proxy = "https://" + proxy.string()
                print("testing", proxy)
                async with session.get(TEST_URL,allow_redirects=False,proxy=real_proxy,timeout=15) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                        print("Available proxy:", proxy)
                    else:
                        self.redis.decrease(proxy)
                        print("Not Available Status:", proxy," Score -1")
            except (aiohttp.ClientError, aiohttp.ClientConnectorError, TimeoutError, AttributeError,aiohttp.ClientOSError, aiohttp.ClientHttpProxyError):
                self.redis.decrease(proxy)
                print("Error detected!", proxy)

    def run(self):
        print("Starts running tester")
        try:
            entries = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(entries), 200):
                test_proxies = entries[i:i + BATCH_TEST_SIZE]
                tasks = [self.single_test(proxy) for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                time.sleep(5)
        except Exception as e:
            print(' Error with tester ', e.args)

if __name__ == '__main__':
    tester = Tester()
    tester.run()


                        