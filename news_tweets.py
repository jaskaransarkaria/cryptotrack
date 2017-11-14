'''Track news headlines and key tweets concerning changes with crypto currencies'''
# google news

import urllib
from urllib.request import urlopen
from bs4 import BeautifulSoup

def make_soup(url): #in order to parse the webpage for info
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data

soup = make_soup('https://news.google.com/news/search/section/q/bitcoin')
bitcoin = soup.find_all("a", class_="nuEeue hzdq5d ME7ew", limit=10)
time_ago = soup.find_all("span", class_="d5kXP YBZVLb", limit=10)

for v, i in zip(bitcoin, time_ago):
    anchor = v.string.strip()
    hyperlink = v.get("href")
    time_stamp = i.string.strip()
    print(anchor + ". " + time_stamp + ".")
    print(hyperlink)

#need to add timed running code