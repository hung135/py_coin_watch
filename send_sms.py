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

phone_list.append(phone)
while (True):
    os.system('clear')
    print(datetime.datetime.utcnow())
    for c in coin_list:
        print(str.replace(c.get_sms_msg(), '\n', ''))
        c.send_sms(server, logon_id, phone_list, send_minutes=20)
    for Coin in coin_list:
        Coin.refresh()
    coin_list.sort(key=lambda Coin: Coin.low_percent, reverse=True)
    time.sleep(40)
# While loop
#
# minimum to sleep for before hitting crypto
secs_min = 60
print("looping Interval.:", secs_min)
while (False):
    secs = secs_min
    print(datetime.datetime.utcnow())

    if (float(ex2.low_percent) < .4):
        print("sending text")
        assert isinstance(server, smtplib)
        server.sendmail(logon_id, phone, ex2.get_sms_msg())
        # what 3 minutes before running again if we send a txt msg out
        secs = secs + secs_min * 15
        print("Sleeping:{} secs".format(secs))
    else:
        print("Not Sending Low Percent:", ex2.low_percent)

    print(ex2.get_sms_msg())
    time.sleep(secs)
    # ex.compare_price(hours=24, market='BTC-NEO')
    # server.sendmail( logon_id, phone, ex2.get_sms_msg())
