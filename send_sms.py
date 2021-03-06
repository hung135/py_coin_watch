import os, datetime, time, sys
from crypto import Exchange, Rule, Coin
from twilio import rest as TwilioClient
from crypto.symbol import SymbolStruct
# import scrape

import scrape

news_list = dict()
last_scrape = None

def scrape_coins(last_scrape,coin_list=dict()):
    assert isinstance(coin_list,dict)
    last_time_threshold = (datetime.datetime.now() - datetime.timedelta(minutes=30))
    if last_scrape is None or last_scrape<last_time_threshold:

        for key,value in coin_list.items():
            assert isinstance(value,Coin)
            l, s = scrape.get_news(value.name,value.symbol)
            news_list[s] = l
        return datetime.datetime.now()
    return last_scrape


# Establish a secure session with gmail's outgoing SMTP server using your gmail account
# server = smtplib.SMTP("smtp.gmail.com", 587)

# server.starttls()

logon_id = os.getenv('logon_id')
logon_pwd = os.getenv('logon_pwd')
binance_api = os.getenv('api_key')
binacne_secret = os.getenv('secret_key')
twilio_sid = os.getenv('twilio_sid')
twilio_token = os.getenv('twilio_token')
cryptopia_api = os.getenv('cryptopia_api')
cryptopia_secret = os.getenv('cryptopia_secret')

server = TwilioClient.Client(twilio_sid, twilio_token)
phone = os.getenv('phone')
from_phone = os.getenv('from_phone')
cryptopia = Exchange(cryptopia_api, cryptopia_secret, Exchange.EX_CRYPTOPIA)
binance = Exchange(binance_api, binacne_secret, Exchange.EX_BINANCE)
bittrex = Exchange(binance_api, binacne_secret, Exchange.EX_BITTREX)

yobit = Exchange(binance_api, binacne_secret, Exchange.EX_YOBIT)

poloniex = Exchange(binance_api, binacne_secret, Exchange.EX_POLONIEX)
binance.add_coin_symbol('ICX', 'BTC', all_exchange=False,name='ICON')
binance.add_coin_symbol('VEN', 'BTC', all_exchange=False,name='VeChain')
binance.add_coin_symbol('BTC', 'USDT', all_exchange=False,name='Bitcoin')
binance.add_coin_symbol('TRX', 'BTC', all_exchange=False,name='TRON')

binance.add_coin_symbol('LTC', 'BTC', all_exchange=False,name='Litecoin')
binance.add_coin_symbol('EOS', 'BTC', all_exchange=False,name='EOS')
binance.add_coin_symbol('ETC', 'BTC', all_exchange=False,name='Ethereum Classic')

poloniex.add_coin_symbol('SC', 'BTC', all_exchange=False,name='Siacoin')
binance.add_coin_symbol('WABI', 'BTC', all_exchange=False,name='WaBi')

binance.add_coin_symbol('ADA', 'BTC', all_exchange=False,name='Cardano')
binance.add_coin_symbol('NANO', 'BTC', all_exchange=False,name='Nano')
bittrex.add_coin_symbol('REP','BTC',all_exchange=False,name='Augur')
bittrex.add_coin_symbol('XVG','BTC',all_exchange=False,name='Verge')
binance.add_coin_symbolV2(SymbolStruct('DGD', 0, 'BTC', '<<<', all_exchange=False,name='DigixDAO'))
cryptopia.add_coin_symbolV2(SymbolStruct('LINDA', 0, 'BTC', '<<<', all_exchange=False,name='Linda'))

poloniex.add_coin_symbolV2(SymbolStruct('SC', 0, 'BTC', '<<<', all_exchange=False,name='Siacoin'))

coin_list = binance.create_coin_market()
coin_list.update(bittrex.create_coin_market())
coin_list.update(poloniex.create_coin_market())
coin_list.update(yobit.create_coin_market())
coin_list.update((cryptopia.create_coin_market()))
phone_list = []
phone_list.append(phone)

sleep_time = 60
last_sent = None
last_scrape=scrape_coins(None,coin_list)
while (True):
    os.system('clear')
    # scrape.news_list(yobit)
    connected = False
    print(datetime.datetime.utcnow())
    print(Coin.get_table_header())

    coin_list_sorted = sorted(coin_list.values(), key=lambda x: min([x.low_percent, x.high_percent]), reverse=True)
    # coin_list.sort(key=lambda strky,coin: min([coin.low_percent,coin.high_percent]), reverse=True)
    for c in coin_list_sorted:

        assert isinstance(c, Coin)
        # print(str.replace(c.get_sms_msg(), '\n', ' '))
        news = news_list.get(c.symbol, None)
        c.set_news(news)

        print(c.get_formatted_table_row())

        # run rules add coins to send buffer
        c.fill_send_buffer(delay_minutes=20)
        # run through send buffer to send
        try:
            # if(c.send_sms(server, logon_id, phone_list, send_minutes=20)):
            last_scrape=scrape_coins(last_scrape,coin_list)
            if (c.send_sms(server, from_phone, phone_list, send_minutes=20)):
                if not connected:
                    # server.connect("smtp.gmail.com", 587)
                    pass
                else:
                    connected = True
        except Exception as e:
            print(e)
            # server.connect("smtp.gmail.com", 587)
            connected = True
            # server = smtplib.SMTP("smtp.gmail.com", 587)
            # c.send_sms(server, logon_id, phone_list, send_minutes=20)

    print(time.ctime())
    # print("--------",c.last_sent)
    # print("--------",c.send_buffer)
    for str_key, coin in coin_list.items():
        coin.refresh()

    sys.stdout.write("|")
    for l in range(sleep_time):
        sys.stdout.write("-")
    sys.stdout.write("|\n")
    sys.stdout.flush()
    sys.stdout.write("|")
    # print(scrape.get_news('TRON', 'TRX'))
    for l in range(sleep_time):
        sys.stdout.write(">")
        sys.stdout.flush()
        time.sleep(1)
# While loop
