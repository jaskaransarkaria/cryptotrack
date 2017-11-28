'''track cryptocurrencies on the stock markets'''
import coinmarketcap
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup


def make_soup(url): #in order to parse the webpage for info
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data

def coin_info(coin): # parse the top ten news for each coin
    coinsoup = make_soup('https://news.google.com/news/search/section/q/' + coin)
    coin = coinsoup.find_all("a", class_="nuEeue hzdq5d ME7ew", limit=10)
    time_ago = coinsoup.find_all("span", class_="d5kXP YBZVLb", limit=10)

    for v, i in zip(coin, time_ago): # print coin and time tag simultaneously
        anchor = v.string.strip()
        hyperlink = v.get("href")
        time_stamp = i.string.strip()
        print(anchor + ". " + time_stamp + ".")
        print(hyperlink)

def coin_price(coin): # connect to api(coinmarketcap.com) and print info
    market = coinmarketcap.Market()
    currency = market.ticker(coin)
    price_table = pd.Series((currency)[0]) #need to format and cut out unneeded data from this pandas
    price_table = price_table.reindex(["name", "rank", "symbol", "price_usd", "price_btc", "percent_change_1h", "percent_change_24h", "percent_change_7d"])
    print(price_table)

def coin_and_news():
    coin_price("bitcoin")
    print("\n")
    coin_info("bitcoin")
    print("\n")
    print("\n")
    print("\n")
    coin_price("ethereum")
    print("\n")
    coin_info("ethereum")
    print("\n")
    print("\n")
    print("\n")
    coin_price("iota")
    print("\n")
    coin_info("iota")
    print("\n")
    print("\n")
    print("\n")
    print("\n")
    print("\n")

sched = BlockingScheduler()
sched.add_job(coin_and_news, 'cron', hour='10-22', minute='0,15,30,45') # scheduled to run between the hours 10 and 10pm
sched.start()