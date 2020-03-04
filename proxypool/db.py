MAX_SCORE = 100
MIN_SCORE = 0
INI_SCORE = 10
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PWD = None
REDIS_KEY = "proxies"

import redis
from random import choice
from exceptions import PoolEmptyError

REDIS_CLIENT_VERSION = redis.__version__
IS_REDIS_VERSION_2 = REDIS_CLIENT_VERSION.startswith('2.')

class RedisClient():
    def __init__(self, host = REDIS_HOST, port = REDIS_PORT, pwd = REDIS_PWD):
        self.db = redis.StrictRedis(host=host,port=port,password=pwd,decode_responses=True)
    
    def add(self, proxy, score = INI_SCORE):
        # if proxy not in db, store it
        if not self.db.zscore(REDIS_KEY, proxy):
            if IS_REDIS_VERSION_2:
                res = self.db.zadd(REDIS_KEY, score, proxy)
            else:
                res = self.db.zadd(REDIS_KEY, {proxy:score})
            # print(res)
            return res
    
    def random(self):
        # try to get the proxies with MAX_SCORE
        # if doesn't have one, return all entries
        ret = self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(ret) > 0:
            return choice(ret)
        else:
            ret = self.db.zrevrange(REDIS_KEY,MIN_SCORE,MAX_SCORE)
            if len(ret) > 0:
                return choice(ret)
            else:
                raise PoolEmptyError
    
    def decrease(self, proxy):
        # proxy = proxy.string()
        score = self.db.zscore(REDIS_KEY, proxy)
        # current score is larger than PROXY_SCORE_MIN
        if score and score > MIN_SCORE:
            if IS_REDIS_VERSION_2:
                return self.db.zincrby(REDIS_KEY, proxy, -1)
            return self.db.zincrby(REDIS_KEY, -1, proxy)
        else:
            self.db.zrem(REDIS_KEY, proxy)
    
    def exists(self, proxy):
        # check if proxy exists in database
        return not self.db.zscore(REDIS_KEY,proxy) == None
    
    def max(self, proxy):
        # set available proxy's score to 100
        print("Proxy ", proxy, " is available, sets score as 100")
        return self.db.zadd(REDIS_KEY, proxy, MAX_SCORE)
    
    def count(self):
        # return number of elements
        return self.db.zcard(REDIS_KEY)

    def all(self):
        # return all elements
        return self.db.zrevrange(REDIS_KEY, MIN_SCORE, MAX_SCORE)    

tmp = RedisClient()
print(tmp.count())