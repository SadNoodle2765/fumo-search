import time
import requests
import os
from bs4 import BeautifulSoup


import fumoDB
from fumo import FumoItem, FumoAuctionItem

import random

user_agent_list = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:59.0) Gecko/20100101 Firefox/59.0'
]


HEADERS = {    
    'User-Agent': random.choice(user_agent_list)
}

def changeHeaders():
    global HEADERS

    HEADERS = {    
        'User-Agent': random.choice(user_agent_list)
    }

# HEADERS = {
#     'User-Agent': 'NonProfit-FumoBot (arceus3333@gmail.com)'
# }

BASE_URL_BUYEE =  'https://buyee.jp'
BASE_URL_AUCTION = 'https://buyee.jp/item/search/query/??????%20????????????'
BASE_URL_SHOPPING = 'https://buyee.jp/category/yahoo/shopping/2134?query=??????+????????????'
BASE_URL_MERCARI = 'https://buyee.jp/mercari/search?keyword=??????+????????????'
BASE_URL_RAKUMA = 'https://buyee.jp/rakuma/search?keyword=??????+????????????'

DELAY_TIME = 1


_BANNED_KEYWORDS = ['??????????????????', '?????????', '????????????', '?????????', '??????????????????', '?????????', '????????????', 'CAN', '?????????', '????????????'] # Keyholder, Strap, Rubber, Acrylic, Mug, Mousepad, Towel, Illustrate

# If a product isn't a fumo, like a keyholder or a mousepad, the title should hopefully say it and this function will catch it
def isFumoTitle(title):
    for keyword in _BANNED_KEYWORDS:
        if keyword in title:
            return False
    
    return '??????' in title or ('??????' in title and '???????????????' in title)         # Final check to see if title actually has "fumo" in it

def parseYahooAuction(soup) -> list[FumoAuctionItem]:
    fumoItems = list()
    itemCards = soup.find_all('li', class_='itemCard')

    for itemCard in itemCards:
        title = itemCard.select_one('.itemCard__itemName>a').text.strip()

        if not isFumoTitle(title):                                                               # Removes non-fumo products
            continue

        prices = itemCard.select('.g-priceDetails__item>div>.g-price')
        curPrice = int(prices[0].text[:-4].replace(',', ''))                                     # From "7,000 yen" to 7000
        buyoutPrice = int(prices[1].text[:-4].replace(',', '')) if len(prices) > 1 else 0
        buyLink = BASE_URL_BUYEE + itemCard.select_one('.itemCard__itemName>a').attrs['href']
        buyLink = buyLink.split('?')[0]                                                          # Removes the extra query

        # itemInfo = itemCard.select('.itemCard__infoList>.itemCard__infoItem>.g-text')

        imgLink = itemCard.find('img', class_='hide g-thumbnail__image').attrs['data-src']
        imgLink = imgLink.split('?')[0]                                                          # Removes the extra query

        fumoItem = FumoAuctionItem(title, curPrice, buyoutPrice, buyLink, imgLink)

        fumoItems.append(fumoItem)

    return fumoItems


def getFromYahooAuction():
    response = requests.get(BASE_URL_AUCTION, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    numOfPages = 0
    try:
        numOfPages = soup.select('.page_navi>a')[-1].attrs['data-bind']
    except:
        print(response.content)
        return False

    numOfPages = soup.select('.page_navi>a')[-1].attrs['data-bind']
    startIndex = numOfPages.find('"page"') + 7
    endIndex = numOfPages.find(',"rc"')
    numOfPages = int(numOfPages[startIndex:endIndex])

    # fumoFile = open('fumos.txt', 'w', encoding='utf8')

    fumoItems = list()

    print('Getting page 1')

    for page in range(2, numOfPages+1):
        fumoItems += parseYahooAuction(soup)

        # for item in fumoItems:
        #     fumoFile.write(str(item))
        #     fumoFile.write('-------------------------------------------------\n')

        time.sleep(DELAY_TIME)                                                                       # Waiting to preserve politeness

        print(f'Getting page {page}')
        response = requests.get(BASE_URL_AUCTION + f'?page={page}', headers=HEADERS)            # Getting data from next page
        soup = BeautifulSoup(response.text, 'html.parser')

    fumoItems += parseYahooAuction(soup)        # Getting the last page, since it wasn't included in for loop
    
    return fumoItems
    # fumoFile.close()
    # print(numOfPages)

def parseYahooShopping(soup) -> list[FumoItem]:
    fumoItems = list()
    itemCards = soup.find_all('li', class_='product_whole')

    for itemCard in itemCards:
        title = itemCard.select_one('.product_info>.product_title>span').text

        if not isFumoTitle(title):                                                               # Removes non-fumo products
            continue

        print(title)

        price = int(itemCard.select_one('a').attrs['data-price'])

        buyLink = BASE_URL_BUYEE + itemCard.select_one('a').attrs['href']
        buyLink = buyLink.split('?')[0]                                                          # Removes the extra query


        imgLink = itemCard.find('img', class_='hide').attrs['data-src']

        fumoItem = FumoItem(title, price, buyLink, imgLink)

        fumoItems.append(fumoItem)

    return fumoItems

def getFromYahooShopping():
    response = requests.get(BASE_URL_SHOPPING, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    numOfPages = 0
    try:
        numOfPages = soup.select('.page_navi>a')[-1].attrs['onclick']
    except:
        print(response.status_code)
        return False
    
    startIndex = numOfPages.find('page.value')+13
    endIndex = numOfPages.find(';')
    numOfPages = int(numOfPages[startIndex:endIndex])

    fumoItems = list()

    print('Getting page 1')

    for page in range(2, numOfPages+1):
        fumoItems += parseYahooShopping(soup)

        time.sleep(DELAY_TIME)                                                                       # Waiting to preserve politeness

        print(f'Getting page {page}')
        response = requests.get(BASE_URL_SHOPPING + f'&page={page}', headers=HEADERS)            # Getting data from next page
        soup = BeautifulSoup(response.text, 'html.parser')
    
    fumoItems += parseYahooShopping(soup)        # Getting the last page, since it wasn't included in for loop
    
    return fumoItems


def parseStore(soup):
    fumoItems = list()
    itemCards = soup.select('.item-lists>li')

    for itemCard in itemCards:
        title = itemCard.find('h2').text
        
        if not isFumoTitle(title):                                                               # Removes non-fumo products
            continue

        if itemCard.find('div', class_='soldOut__text'):                                         # Removes ones that are sold out
            continue

        price = int(itemCard.find('p', class_='price').text[:-4].replace(',',''))                    # From "7,000 yen" to 7000
        buyLink = itemCard.find('a').attrs['href']
        buyLink = BASE_URL_BUYEE + buyLink.split('?')[0]        # Remove query part

        imgLink = itemCard.find('img').attrs['data-bind']
        startIndex = imgLink.find("imagePath: '") + 12
        endIndex = startIndex + imgLink[startIndex:].find("',")
        imgLink = 'https:' + imgLink[startIndex:endIndex]

        fumoItem = FumoItem(title, price, buyLink, imgLink)
        fumoItems.append(fumoItem)

    return fumoItems

# Works for Mercari and Rakuma, only base url is different
def getFromStore(base_url: str):
    response = requests.get(base_url, headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')

    numOfPages = 0
    try:
        numOfPages = soup.select('.pagination-outer>.pagination>li>a')[-1]
    except:
        print(response.content)
        return False

    startIndex = numOfPages.attrs['href'].find('page=') + 5
    numOfPages = int(numOfPages.attrs['href'][startIndex:])
    
    fumoItems = list()

    print('Getting page 1')

    for page in range(2, numOfPages+1):
        fumoItems += parseStore(soup)

        time.sleep(DELAY_TIME)                                                                       # Waiting to preserve politeness

        print(f'Getting page {page}')
        response = requests.get(base_url + f'&page={page}', headers=HEADERS)            # Getting data from next page
        soup = BeautifulSoup(response.text, 'html.parser')


    fumoItems += parseStore(soup)

    return fumoItems

    # numOfPages = int(numOfPages[numOfPages.find('"page"') + 7])


def updateRecords():
    # if os.path.exists('fumoFile.txt'):                                      # File that stores info on fumo items
    #     os.remove('fumoFile.txt')

    RESTART_WAIT_TIME = 20

    auctionItems = mercariItems = rakumaItems = False

    for i in range(5):
        print('Pulling from Yahoo Auction')
        auctionItems = getFromYahooAuction()

        if auctionItems:
            print("Pulled successfully")
            break

        print('Failed pulling from auction. Trying again in 20 seconds')
        changeHeaders()
        time.sleep(RESTART_WAIT_TIME)


    for i in range(5):
        print('Pulling from Yahoo Shopping')
        shoppingItems = getFromYahooShopping()

        if shoppingItems:
            print("Pulled successfully")
            break

        print("Failed pulling from shopping. Trying again in 20 seconds")
        changeHeaders()
        time.sleep(RESTART_WAIT_TIME)


    for i in range(5):
        print('Pulling from Mercari')
        mercariItems = getFromStore(BASE_URL_MERCARI)

        if mercariItems:
            print("Pulled successfully")
            break

        print('Failed pulling from Mercari. Trying again in 02 seconds')
        changeHeaders()
        time.sleep(RESTART_WAIT_TIME)

    for i in range(5):
        print('Pulling from Rakuma')
        rakumaItems = getFromStore(BASE_URL_RAKUMA)

        if rakumaItems:
            print("Pulled successfully")
            break

        print('Failed pulling from Rakuma. Trying again in 20 seconds')
        changeHeaders()
        time.sleep(RESTART_WAIT_TIME)


    

    if auctionItems and shoppingItems and mercariItems and rakumaItems:
        fumoDB.dropFumoData()
        fumoDB.updateFumoDB(auctionItems, isAuction=True)
        fumoDB.updateFumoDB(shoppingItems, isAuction=False)
        fumoDB.updateFumoDB(mercariItems, isAuction=False)
        fumoDB.updateFumoDB(rakumaItems, isAuction=False)

    # with open('soup.txt', 'w', encoding='utf8') as file:                # Storing data
    #     file.write(soup.prettify())


    # itemCards = soup.find_all('li', class_='itemCard')


    # with open('fumoFile.txt', 'a', encoding='utf8') as file:
    #     for itemCard in itemCards:
    #         itemName = itemCard.select_one('.itemCard__itemName>a').text
    #         itemName = itemName.strip()
    #         file.write(itemName + '\n')

if __name__ == '__main__':
    response = requests.get('https://buyee.jp/item/search/yahoo/shopping?query=??????%20????????????%20?????????', headers=HEADERS)
    soup = BeautifulSoup(response.text, 'html.parser')
    fumoItems = parseYahooShopping(soup)
    for fumo in fumoItems:
        print(fumo.fumoType)