'''track cryptocurrencies on the stock markets'''
import coinmarketcap
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from twilio.rest import Client

def make_soup(url): #in order to parse the webpage for info
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data

def coin_info(coin): # parse the top ten news for each coin
    coinsoup = make_soup('https://news.google.com/news/search/section/q/' + coin)
    coin = coinsoup.find_all("a", class_="nuEeue hzdq5d ME7ew", limit=8)
    time_ago = coinsoup.find_all("span", class_="d5kXP YBZVLb", limit=8)
    total_news = "\n"

    for v, i in zip(coin, time_ago):#print coin and time tag simultaneously
        anchor = v.string.strip()
        hyperlink = v.get("href")
        time_stamp = i.string.strip()
        news = '{}'.format(anchor) + '. ' + '{}'.format(time_stamp) + '.' + '\n' + '{}'.format(hyperlink) + '\n'

        total_news += news #can't send over 1600 char limit per message re-examine this and split into multiple msgs

    return total_news

def coin_price(coin): # connect to api(coinmarketcap.com) and print info
    market = coinmarketcap.Market()
    currency = market.ticker(coin)
    price_table = pd.Series((currency)[0])
    #reindex to select particular info from pd.Series
    price_table = price_table.reindex(["name", "rank", "symbol", "price_usd", "price_btc",
                                       "percent_change_1h", "percent_change_24h", "percent_change_7d"])
    return price_table

def coin_and_news():
    bit_price = coin_price("bitcoin")
    eth_price = coin_price("ethereum")
    iota_price = coin_price("iota")

    #string formation needed as twilio body req string
    textable = '\n' + '{}'.format(bit_price) + '\n' + '\n' + '\n' + \
               '{}'.format(eth_price) + '\n' + '\n' + '\n' +\
               '{}'.format(iota_price) + '\n' + '\n' + '\n'

    return textable #return > print when passing to another program

def send_txt(body):
    account_sid = "AC856ab82823f898863429b9747c4fe9a2"
    auth_token = "aea6dc6c638f7941aa0172d97ecda2a5"
    client = Client(account_sid, auth_token)
    client.messages.create(
        to="+447816179261",
        from_="+441578930046",
        body=body) # string req

def send_coin():
    price = print(coin_and_news())
    return price

def send_bit_news():
    bit_news = print(coin_info("bitcoin"))
    return bit_news

def send_eth_news():
    eth_news = print(coin_info("ethereum"))
    return eth_news

def send_iota_news():
    iota_news = print(coin_info("iota"))
    return iota_news


sched = BlockingScheduler()
sched.add_job(send_coin, 'cron', hour='10-22', minute='3,18,33,48')#scheduled to run between the hours 10 and 10pm
#sched.add_job(send_bit_news, 'cron', hour='10-22', minute='2,17,32,47') #need to add seconds
#sched.add_job(send_eth_news, 'cron', hour='10-22', minute='1,16,31,46')
#sched.add_job(send_iota_news, 'cron', hour='10-22', minute='0,15,30,45')
sched.start()