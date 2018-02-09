
import smtplib
import os
from exchange import Exchange as zz

# Establish a secure session with gmail's outgoing SMTP server using your gmail account
server = smtplib.SMTP( "smtp.gmail.com", 587 )

server.starttls()
logon_id=os.getenv('logon_id')
logon_pwd=os.getenv('logon_pwd')
phone=os.getenv('phone')
print(logon_id)
print(logon_pwd)
server.login(logon_id, logon_pwd)

# Send text message through SMS gateway of destination number

z=zz(exchange='YOBIT',coin_str='BTC')
print(str(z.msg))

#server.sendmail( logon_id, phone, str(z.msg))

