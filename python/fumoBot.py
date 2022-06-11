from heapq import merge
import time
import requests
import os
from bs4 import BeautifulSoup


import fumoDB
from fumo import FumoItem, FumoAuctionItem

import random

from fake_useragent import UserAgent
ua = UserAgent(use_cache_server=False)


HEADERS = {    
    'User-Agent': ua.random
}

# HEADERS = {
#     'User-Agent': 'NonProfit-FumoBot (arceus3333@gmail.com)'
# }

BASE_URL_BUYEE =  'https://buyee.jp'
BASE_URL_AUCTION = 'https://buyee.jp/item/search/query/東方%20ふもふも'
BASE_URL_MERCARI = 'https://buyee.jp/mercari/search?keyword=東方+ふもふも'
BASE_URL_RAKUMA = 'https://buyee.jp/rakuma/search?keyword=東方+ふもふも'

DELAY_TIME = 3


_BANNED_KEYWORDS = ['キーホルダー', 'ラバー', 'アクリル', '湯のみ', 'マウスパッド', 'タオル', 'イラスト', 'CAN', 'マット', 'コスプレ'] # Keyholder, Strap, Rubber, Acrylic, Mug, Mousepad, Towel, Illustrate

# If a product isn't a fumo, like a keyholder or a mousepad, the title should hopefully say it and this function will catch it
def isFumoTitle(title):
    for keyword in _BANNED_KEYWORDS:
        if keyword in title:
            return False
    
    return 'ふも' in title or ('東方' in title and 'ぬいぐるみ' in title)         # Final check to see if title actually has "fumo" in it

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

def getFromYahooShopping():
    pass

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

    print('Pulling from Yahoo Auction')
    auctionItems = getFromYahooAuction()

    # print('Pulling from Yahoo Shopping')
    # getFromYahooShopping()
    
    print('Pulling from Mercari')
    mercariItems = getFromStore(BASE_URL_MERCARI)

    print('Pulling from Rakuma')
    rakumaItems = getFromStore(BASE_URL_RAKUMA)

    if auctionItems and mercariItems and rakumaItems:
        fumoDB.dropFumoData()
        fumoDB.updateFumoDB(auctionItems, isAuction=True)
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

def testUpdateRecords():
    TEMP_WEBPAGE = open('soup.txt', 'r', encoding='utf8').read()
    soup = BeautifulSoup(TEMP_WEBPAGE, 'html.parser')

    itemCards = soup.find_all('li', class_='itemCard')

    if os.path.exists('fumoFile.txt'):
        os.remove('fumoFile.txt')

    with open('fumoFile.txt', 'a', encoding='utf8') as file:
        for itemCard in itemCards:
            itemName = itemCard.select_one('.itemCard__itemName>a').text
            itemName = itemName.strip()
            file.write(itemName + '\n')