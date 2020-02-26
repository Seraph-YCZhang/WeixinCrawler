from pyquery import PyQuery as pq
import requests
class ProxyMetaclass(type):
    def __new__(cls, name, bases, attrs):
        count = 0
        attrs["__CrawlFunc__"] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                 attrs["__CrawlFunc__"].append(k)
                 count += 1
        attrs["__CrawlFuncCounts__"] = count
        return type.__new__(cls, name, bases, attrs)

class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):
            print("Successfully get proxy",proxy)
            proxies.append(proxy)
        return proxies
    
    def get_page(self,url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    def crawl_kuaidaili(self):
        page_count = 200
        start_url = 'https://www.kuaidaili.com/free/inha/{page}/'
        urls = [start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print("Crawling...")
            html = self.get_page(url)
            if html:
                doc = pq(html)

        
