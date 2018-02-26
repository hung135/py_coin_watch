import re
import requests
import pandas as pd
from bs4 import BeautifulSoup, element
import urllib
# urllib.parse.unquote(url)
import datetime
import crypto.exchange


def get_news(coin_name, coin_symbol):
    # 14/02/2018
    print("Scraping:",coin_name,coin_symbol)
    start_date = datetime.datetime.now()
    end_date = start_date + datetime.timedelta(days=20)
    coin_list = dict()
    coin_list[coin_name] = coin_symbol

    # coin_list['Siacoin']='SC'

    # coin_param="form[coin][0]={}+({})".format(coin_name,coin_symbol)

    def make_coin_list(coin_list):
        coin_param = "&form[coin][]={}+({})"
        coin_string = ""
        assert isinstance(coin_list, dict)
        # key = Coin Name value = Coin Symbol
        for name, symbol in coin_list.items():
            coin_string = coin_string + coin_param.format(name, symbol)
        return coin_string

    host = 'https://coinmarketcal.com/?'
    param = """form[date_range]={} - {}{}&form[sort_by]=&form[filter_by]=&form[submit]="""
    param = param.format(start_date.strftime('%d/%m/%Y'), end_date.strftime('%d/%m/%Y'), make_coin_list(coin_list))

    url = host + param
    resp = requests.get(url)

    soup = BeautifulSoup(resp.text, 'html.parser')

    # print(soup)
    # divs = soup.find('div', attrs={'class':'content-box-info'})
    divs = soup.find_all("div", class_="content-box-general")
    data_list = []
    for d in divs:
        assert isinstance(d, element.Tag)
        # print(d)
        h5 = d.find('h5')
        assert isinstance(h5, element.Tag)
        atag = h5.a
        # print(atag)

        data_list.append(
            {'data_coin': atag['data-coin'], 'data_date': atag['data-date'], 'data_title': atag['data-title']})

    return data_list,coin_symbol


class news_list():
    def __init__(self, ex):
        assert isinstance(ex, crypto.exchange.Exchange)
        print(ex.get_all_ticker(), "-------")
