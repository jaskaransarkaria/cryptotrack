'''track cryptocurrencies on the stock markets'''
# coinmarketcap.com
import coinmarketcap
import requests
import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from time import sleep


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

def coin_price(coin):
    market = coinmarketcap.Market()
    currency = market.ticker(coin)
    price_table = pd.Series((currency)[0]) #need to format and cut out unneeded data from this pandas
    print(price_table)

    #need to only collect "name", "rank", "price_usd", "percent_change_1hr", "percent_change_24hr"
    # "percent_change_7d"

while True:
    coin_price("bitcoin")
    coin_info("bitcoin")
    print("\n")
    print("\n")
    print("\n")
    coin_price("ethereum")
    coin_info("ethereum")
    print("\n")
    print("\n")
    print("\n")
    coin_price("iota")
    coin_info("iota")
    sleep(3600) # wait 1 hour
