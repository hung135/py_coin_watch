import smtplib, os, datetime, time,sys
from crypto import Exchange, Rule, Coin

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()
logon_id = os.getenv('logon_id')
logon_pwd = os.getenv('logon_pwd')
binance_api = os.getenv('api_key')
binacne_secret = os.getenv('secret_key')

phone = os.getenv('phone')
print(logon_id)
#print(logon_pwd)
server.login(logon_id, logon_pwd)

yobit = Exchange(None, None, Exchange.EX_YOBIT)

yobit.add_coin_symbol('linda','<')


poloniex = Exchange(None, None, Exchange.EX_POLONIEX)



poloniex.add_coin_symbol('SC','<')
poloniex.add_coin_symbol('XRP','<')
binance = Exchange(binance_api, binacne_secret, Exchange.EX_BINANCE)
bittrex = Exchange(binance_api, binacne_secret, Exchange.EX_BITTREX)
binance.add_coin_symbol('VEN','<')
binance.add_coin_symbol('ICX','<')
binance.add_coin_symbol('NANO','<')
binance.add_coin_symbol('TRX','<')
binance.add_coin_symbol('EOS')
bittrex.add_coin_symbol('SC')
bittrex.add_coin_symbol('NEO')
bittrex.add_coin_symbol('IGNIS')
bittrex.add_coin_symbol('NXT')


coin_list = binance.create_coin_market() + bittrex.create_coin_market()+poloniex.create_coin_market() +yobit.create_coin_market()
phone_list = []
phone_list.append(phone)

sleep_time=60
last_sent=None
while (True):
    os.system('clear')
    connected=False
    print(datetime.datetime.utcnow())
    print(Coin.get_table_header())
    coin_list.sort(key=lambda coin: min([coin.low_percent,coin.high_percent]), reverse=True)
    for c in coin_list:
        assert isinstance(c, Coin)
        #print(str.replace(c.get_sms_msg(), '\n', ' '))
        print(c.get_formatted_table_row())

        try:
            if(c.send_sms(server, logon_id, phone_list, send_minutes=20)):
                if not connected:
                    server.connect("smtp.gmail.com", 587)
                else:
                    connected=True
        except:
            server.connect("smtp.gmail.com", 587)
            connected=True
            #server = smtplib.SMTP("smtp.gmail.com", 587)
            #c.send_sms(server, logon_id, phone_list, send_minutes=20)

    for coin in coin_list:
        coin.refresh()

    sys.stdout.write("|")
    for l in range(sleep_time):
        sys.stdout.write("-")
    sys.stdout.write("|\n")
    sys.stdout.flush()
    sys.stdout.write("|")
    for l in range(sleep_time):

        sys.stdout.write(">")
        sys.stdout.flush()
        time.sleep(1)
# While loop
