'''track cryptocurrencies on the stock markets'''
import coinmarketcap
from apscheduler.schedulers.blocking import BlockingScheduler
import pandas as pd
import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup
import smtplib

def make_soup(url): #in order to parse the webpage for i¬nfo
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
        news = '{}'.format(anchor) + '. ' + '{}'.format(time_stamp) + '.' + '\n' +\
               '{}'.format(hyperlink) + '\n' # put in html hyperlink tags

        total_news += news #can't send over 1600 char limit per text message re-examine this and
        # split into multiple msgs (n/a for email)

    return total_news

def coin_price(coin): # connect to api(coinmarketcap.com) and print info
    market = coinmarketcap.Market()
    currency = market.ticker(coin)          # need to select GBP to display price also
    price_table = pd.Series((currency)[0])
    #reindex to select particular info from pd.Series
    price_table = price_table.reindex(["name", "rank", "symbol", "price_usd", "price_btc",
                                       "percent_change_1h", "percent_change_24h", "percent_change_7d"])
    return price_table

def coin_and_news(): #actually just returns price
    bit_price = coin_price("bitcoin")
    eth_price = coin_price("ethereum")
    iota_price = coin_price("iota")
    ripple_price = coin_price("ripple")

    #string formation needed as twilio body req string
    textable = '\n' + '{}'.format(bit_price) + '\n' + '\n' + '\n' + \
               '{}'.format(eth_price) + '\n' + '\n' + '\n' +\
               '{}'.format(iota_price) + '\n' + '\n' + '\n' +\
               '{}'.format(ripple_price) + '\n' + '\n' + '\n'

    return textable #return > print when passing to another program


def email():

    gmail_user = 'everything.crypto.info@gmail.com'
    gmail_pass = 'fuckyourich'

    sent_from = 'everything.crypto.info@gmail.com'
    sent_to = ['jaskaran.sarkaria@googlemail.com', 'simran.sarkaria@gmail.com', 'rav.singh.mann@gmail.com',
               'sarkaria.p@gmail.com']

    coin_stats = coin_and_news()

    bit_info = coin_info("bitcoin") #problem sending hyperlinks
    eth_info = coin_info("ethereum")
    iota_info = coin_info("iota")
    ripple_info = coin_info("ripple")

    all_info = """Crypto information

    Bitcoin information
    {}
    Ehtereum information
    {}
    Iota information
    {}
    Ripple information
    {}""".format(bit_info, eth_info, iota_info, ripple_info)

    email_text = """
            {}
            {}
            """.format(coin_stats, all_info).encode()

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465) #insecure connection created, protocol for mail submission uses 587
        server.ehlo() # identifies me to SMTP server
        server.login(gmail_user, gmail_pass)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print('Email sent!')

    except:
        print('Something went wrong...')

def send_email():
    send_it = email()
    return send_it

sched = BlockingScheduler()
sched.add_job(send_email, 'cron', hour='10-22', minute='0')
sched.start()