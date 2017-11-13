'''Track news headlines and key tweets concerning changes with crypto currencies'''
# google news

import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from selenium import webdriver

def make_soup(url): #in order to parse the webpage for info
    the_page = urllib.request.urlopen(url)
    soup_data = BeautifulSoup(the_page, 'html.parser')
    return soup_data

def click_link(old_link, new_link): #this is for opening headlines... I don't need it atm

    driver = webdriver.chrome()
    driver.get(old_link)
    elem1 = driver.find_element_by_link_text(new_link) #these will be the headlines
    elem1.click()
    current_url = driver.current_url
    driver.implicitly_wait(60)  # 60 seconds
    soup3 = make_soup(current_url)
    soup5 = soup3.get_text()



soup = make_soup('https://news.google.com/news/search/section/q/bitcoin')
for anchor in soup.find_all('a'):
    #elem2 = driver.find_element_by_partial_link_text() #need to find just bitcoin info
    print(anchor.text) # prints ALL anchor tags at the minute I just need the first relevant 5
    html_link = anchor.get("href")
    print(html_link)