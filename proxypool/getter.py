<<<<<<< HEAD
from db import RedisClient
from crawler import Crawler
=======
from proxypool.db import RedisClient
from proxypool.crawler import Crawler
>>>>>>> 59e27b94b8e8476bfa759884a062e68b32d99a7a

POOL_UPPER = 10000
class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
<<<<<<< HEAD
        if self.redis.count() >= POOL_UPPER:
=======
        if self.redis.count >= POOL_UPPER:
>>>>>>> 59e27b94b8e8476bfa759884a062e68b32d99a7a
            return True
        else:
            return False
    
    def run(self):
        print("Starts running crawlers")
        if not self.is_over_threshold():
            for callback_func in self.crawler.__CrawlFunc__:
                proxies = self.crawler.get_proxies(callback_func)
                for proxy in proxies:
<<<<<<< HEAD
                        self.redis.add(proxy)

tmp = Getter()
tmp.run()
=======
                    self.redis.add(proxy)
>>>>>>> 59e27b94b8e8476bfa759884a062e68b32d99a7a
