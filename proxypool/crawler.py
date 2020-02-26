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
    
    def Proxy(self, ip, port):
        return "{}:{}".format(ip,port)

    def get_page(self,url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text

    def crawl_kuaidaili(self):
        page_count = 200
        start_url = 'https://www.kuaidaili.com/free/inha/{}/'
        urls = [start_url.format(page) for page in range(1,page_count+1)]
        for url in urls:
            print("Crawling...")
            html = self.get_page(url)
            if html:
                doc = pq(html)
                for item in doc('table tr').items():
                    td_ip = item.find('td[data-title="IP"]').text()
                    td_port = item.find('td[data-title="PORT"]').text()
                    if td_ip and td_port:
                        yield self.Proxy(ip=td_ip, port=td_port)

        
