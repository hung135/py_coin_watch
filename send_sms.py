import smtplib, os, time
from exchange import Exchange

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()
logon_id = os.getenv('logon_id')
logon_pwd = os.getenv('logon_pwd')
binance_api = os.getenv('api_key')
binacne_secret = os.getenv('secret_key')

phone = os.getenv('phone')
print(logon_id)
print(logon_pwd)
server.login(logon_id, logon_pwd)

# Send text message through SMS gateway of destination number

# ex=Exchange(exchange='BITTREX',market='BTC')
# ex.compare_price(hours=24,market='BTC-BCC')
ex = Exchange(exchange='BINANCE', market='TRXBTC')
#
print(ex.coin.print_price())

# While loop
while (True):
    print("looping...")
    time.sleep(20)
    # ex.compare_price(hours=24, market='BTC-NEO')
# server.sendmail( logon_id, phone, str(z.msg))
