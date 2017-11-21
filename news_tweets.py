'''Track news headlines and key tweets concerning changes with crypto currencies'''
# google news

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

def make_soup(url): #in order to parse the webpage for info
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data

def coin_info(coin):
    coinsoup = make_soup('https://news.google.com/news/search/section/q/' + coin)
    coin = coinsoup.find_all("a", class_="nuEeue hzdq5d ME7ew", limit=10)
    time_ago = coinsoup.find_all("span", class_="d5kXP YBZVLb", limit=10)

    for v, i in zip(coin, time_ago):
        anchor = v.string.strip()
        hyperlink = v.get("href")
        time_stamp = i.string.strip()
        print(anchor + ". " + time_stamp + ".")
        print(hyperlink)



coin_info("bitcoin")
print("\n")
print("\n")
print("\n")
coin_info("ethereum")
print("\n")
print("\n")
print("\n")
coin_info("iota")
#need to add timed running code