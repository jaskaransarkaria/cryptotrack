'''track cryptocurrencies on the stock markets'''
# coinmarketcap.com
import coinmarketcap
import requests
from time import sleep
import pandas as pd

def coin_price(coin):
    market = coinmarketcap.Market()
    currency = market.ticker(coin)
    price_table = pd.Series((currency)[0]) #need to format and cut out unneeded data from this pandas
    print(price_table)

    #need to only collect "name", "rank", "price_usd", "percent_change_1hr", "percent_change_24hr"
    # "percent_change_7d"

while True:
    coin_price("bitcoin")
    print("\n")
    print("\n")
    print("\n")
    coin_price("ethereum")
    print("\n")
    print("\n")
    print("\n")
    coin_price("iota")
    sleep(3600) # 1 hour wait before next stat return