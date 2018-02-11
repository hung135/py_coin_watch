import smtplib, os, datetime, time
from crypto import Exchange, Rule, Coin

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP("smtp.gmail.com", 587)
print(type(server))
server.starttls()
logon_id = os.getenv('logon_id')
logon_pwd = os.getenv('logon_pwd')
binance_api = os.getenv('api_key')
binacne_secret = os.getenv('secret_key')

phone = os.getenv('phone')
print(logon_id)
print(logon_pwd)
server.login(logon_id, logon_pwd)

binance = Exchange(binance_api, binacne_secret, Exchange.EX_BINANCE)
bittrex = Exchange(binance_api, binacne_secret, Exchange.EX_BITTREX)
binance.add_coin_symbol('VEN')
binance.add_coin_symbol('ICX')
binance.add_coin_symbol('NANO')
binance.add_coin_symbol('TRX')

bittrex.add_coin_symbol('SC')
bittrex.add_coin_symbol('NEO')
bittrex.add_coin_symbol('IGNIS')
coin_list = binance.create_coin_market() + bittrex.create_coin_market()
phone_list = []
phone_list.append(phone)

sleep_time=60
last_sent=None
while (True):
    os.system('clear')
    connected=False
    print(datetime.datetime.utcnow())

    for c in coin_list:
        print(str.replace(c.get_sms_msg(), '\n', ' '))
        try:
            if(c.send_sms(server, logon_id, phone_list, send_minutes=20)):
                if not connected:
                    server.connect("smtp.gmail.com", 587)
                else:
                    connected=True
        except:
            server.connect("smtp.gmail.com", 587)
            #server = smtplib.SMTP("smtp.gmail.com", 587)
            #c.send_sms(server, logon_id, phone_list, send_minutes=20)

    for Coin in coin_list:
        Coin.refresh()
    coin_list.sort(key=lambda Coin: Coin.low_percent, reverse=True)
    time.sleep(sleep_time)
# While loop
