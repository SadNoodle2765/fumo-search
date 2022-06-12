import requests
from bs4 import BeautifulSoup
from itertools import cycle
import random

src = 'https://en.wikipedia.org/'
response = requests.get('https://free-proxy-list.net/')       
soup = BeautifulSoup(response.text, 'html.parser')


proxies = soup.find('textarea').text[74:].strip().split()
random.shuffle(proxies)

if proxies:
    for proxy in proxies:
        try:
            r = requests.get(src, proxies={"http": proxy, "https": proxy})
            file_request_succeed = r.ok
            if file_request_succeed:                                    
                print('Rotated IP %s succeed' % proxy)                                    
                break
        except Exception as e:                                
            print('Rotated IP %s failed (%s)' % (proxy, str(e)))

# proxies = set()
# for i in parser.xpath('//tbody/tr'):
#   if i.xpath('.//td[7][contains(text(),"yes")]'):                            
#     proxy = ":".join([i.xpath('.//td[1]/text()')[0], 
#                       i.xpath('.//td[2]/text()')[0]])                            
#     proxies.add(proxy)

# if proxies:
#   proxy_pool = cycle(proxies)
#   for i in range(1, len(proxies)):
#     proxy = next(proxy_pool)
#     try:
#       r = requests.get(src, proxies={"http": proxy, "https": proxy})
#       file_request_succeed = r.ok
#       if file_request_succeed:                                    
#         print('Rotated IP %s succeed' % proxy)                                    
#         break
#     except Exception as e:                                
#       print('Rotated IP %s failed (%s)' % (proxy, str(e)))