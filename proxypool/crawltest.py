import requests
from pyquery import PyQuery as pq

def crawl_kuaidaili():
    page_count = 5
    start_url = 'https://www.kuaidaili.com/free/inha/{}/'
    urls = [start_url.format(page) for page in range(1,page_count+1)]
    for url in urls:
        print("Crawling...")
        html = requests.get(url).text
        if html:
            doc = pq(html)
            for item in doc('table tr').items():
                td_ip = item.find('td[data-title="IP"]').text()
                td_port = item.find('td[data-title="PORT"]').text()
                if td_ip and td_port:
                    # yield Proxy(host=td_ip, port=td_port)
                    print(td_ip,td_port)
crawl_kuaidaili();