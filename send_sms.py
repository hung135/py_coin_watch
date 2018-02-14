import os, datetime, time,sys
from crypto import Exchange, Rule, Coin
from twilio import rest as TwilioClient
from crypto.symbol import SymbolStruct




# Establish a secure session with gmail's outgoing SMTP server using your gmail account
# server = smtplib.SMTP("smtp.gmail.com", 587)

# server.starttls()

logon_id = os.getenv('logon_id')
logon_pwd = os.getenv('logon_pwd')
binance_api = os.getenv('api_key')
binacne_secret = os.getenv('secret_key')
twilio_sid=os.getenv('twilio_sid')
twilio_token=os.getenv('twilio_token')
cryptopia_api =os.getenv('cryptopia_api')
cryptopia_secret=os.getenv('cryptopia_secret')


server = TwilioClient.Client(twilio_sid,twilio_token)
phone = os.getenv('phone')
from_phone = os.getenv('from_phone')
cryptopia = Exchange(cryptopia_api, cryptopia_secret,Exchange.EX_CRYPTOPIA)
binance = Exchange(binance_api, binacne_secret, Exchange.EX_BINANCE)
bittrex = Exchange(binance_api, binacne_secret, Exchange.EX_BITTREX)

yobit = Exchange(binance_api, binacne_secret, Exchange.EX_YOBIT)

poloniex = Exchange(binance_api, binacne_secret, Exchange.EX_POLONIEX)
binance.add_coin_symbol('ICX','BTC',all_exchange=False)
binance.add_coin_symbol('VEN','BTC',all_exchange=False)

binance.add_coin_symbol('TRX','BTC',all_exchange=False)

binance.add_coin_symbol('NANO','BTC',all_exchange=False)
binance.add_coin_symbol('ADA','BTC',all_exchange=False)

binance.add_coin_symbolV2(SymbolStruct('DGD', 0, 'BTC', '<<<', all_exchange=False))
cryptopia.add_coin_symbolV2(SymbolStruct('ZCL', 0, 'BTC', '<<<', all_exchange=False))

poloniex.add_coin_symbolV2(SymbolStruct('SC', 0, 'BTC', '<<<', all_exchange=False))







coin_list = binance.create_coin_market()
coin_list.update(bittrex.create_coin_market())
coin_list.update(poloniex.create_coin_market())
coin_list.update(yobit.create_coin_market())
coin_list.update((cryptopia.create_coin_market()))
phone_list = []
phone_list.append(phone)

sleep_time=60
last_sent=None
while (True):
    os.system('clear')
    connected=False
    print(datetime.datetime.utcnow())
    print(Coin.get_table_header())

    coin_list_sorted = sorted(coin_list.values(), key=lambda x: min([x.low_percent, x.high_percent]), reverse=True)
    #coin_list.sort(key=lambda strky,coin: min([coin.low_percent,coin.high_percent]), reverse=True)
    for c in coin_list_sorted:

        assert isinstance(c, Coin)
        #print(str.replace(c.get_sms_msg(), '\n', ' '))
        print(c.get_formatted_table_row())

        # run rules add coins to send buffer
        c.fill_send_buffer(delay_minutes=20)
        # run through send buffer to send
        try:
            #if(c.send_sms(server, logon_id, phone_list, send_minutes=20)):
            if  (c.send_sms(server, from_phone, phone_list, send_minutes=20)):
                if not connected:
                    #server.connect("smtp.gmail.com", 587)
                    pass
                else:
                    connected=True
        except Exception as e:
            print(e)
            #server.connect("smtp.gmail.com", 587)
            connected=True
            #server = smtplib.SMTP("smtp.gmail.com", 587)
            #c.send_sms(server, logon_id, phone_list, send_minutes=20)

    print(time.ctime())
    # print("--------",c.last_sent)
    #print("--------",c.send_buffer)
    for str_key,coin in coin_list.items():
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
