import scrape
import pprint as pp

import scrape
import arrow
news_list= dict()
def scrape_coins():
    """
    l,s = scrape.get_news('TRON', 'TRX')
    news_list[s]=l

    l,s = scrape.get_news('Cardano', 'ADA')
    news_list[s]=l
    l,s = scrape.get_news('VeChain', 'VEN')
    news_list[s]=l

    l,s = scrape.get_news('WaBi', 'WABI')
    news_list[s]=l

    l,s = scrape.get_news('Bitcoin', 'BTC')
    news_list[s]=l
    l,s = scrape.get_news('Nano', 'NANO')
    news_list[s]=l"""
    l,s = scrape.get_news('Litecoin', 'LTC')
    news_list[s]=l
    l,s = scrape.get_news('ZClassic', 'ZCL')
    news_list[s]=l
#scrape_coins()
pp.pprint(news_list)
ΩΩΩ

from termcolor import colored

print colored('hello', 'red'), colored('world', 'green')