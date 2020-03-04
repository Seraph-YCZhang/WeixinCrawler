from db import RedisClient
from crawler import Crawler

POOL_UPPER = 1000
class Getter():
    def __init__(self):
        self.redis = RedisClient()
        self.crawler = Crawler()

    def is_over_threshold(self):
        if self.redis.count() >= POOL_UPPER:
            return True
        else:
            return False
    
    def run(self):
        print("Starts running crawlers")
        if not self.is_over_threshold():
            for callback_func in self.crawler.__CrawlFunc__:
                proxies = self.crawler.get_proxies(callback_func)
                for proxy in proxies:
                        self.redis.add(proxy)


if __name__ == '__main__':
    getter = Getter()
    getter.run()
