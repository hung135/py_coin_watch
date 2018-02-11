import datetime
import pprint as pp
import smtplib

import crypto


class Coin:
    msg = "{}->{}\nB{}\nA{} \nPrev {}\nL {}\nH {}\nL{}% H{}%\nQTY {}"
    bid = 0
    sell = 0
    last = 0
    market = None
    symbol = None
    exchange_name = None
    exchange_conn = None
    low_percent = 100
    high_percent = 0
    price_yesterday = 0
    price_low_24hr = 0
    price_high_24hr = 0
    hodl=0
    send_history = []
    last_sent = None
    rule_list = set()

    def __init__(self, coin_market, exchange_obj, symbol=None,hodl=0):
        self.market = coin_market
        self.symbol = symbol
        self.hodl=hodl
        self.rule_list.add(crypto.Rule.check_24hr_low)
        self.rule_list.add(crypto.Rule.check_24hr_high)
        assert isinstance(exchange_obj, crypto.Exchange)
        self.exchange_name = exchange_obj.exchange_name
        self.exchange_conn = exchange_obj
        self.refresh()

    def fill_data(self, json):

        if type(json) is not dict:
            raise Exception("json must be type dict")

        if type(self.exchange_conn.exchange_map) is not dict:
            raise Exception("exchange_map must be type dict")
        # looks through json and pulls fields that matches the mapping and set the instance variable

        for key, val in self.exchange_conn.exchange_map.items():
            value = json.get(val, 0)
            if value != 0:
                setattr(self, key, value)
        self.low_percent = float(crypto.Rule.get_delta_24hr_low(self))
        self.high_percent = float(crypto.Rule.get_delta_24hr_high(self))

    def refresh(self):
        try:
            self.fill_data(self.exchange_conn.get_coin_data_json(self))
        except Exception as e:
            print("Error Filling Data:",e)
    def send_sms(self, server, sender, phone_list, send_minutes=30):
        send = False
        assert isinstance(phone_list, list)

        last_time_threshold = (datetime.datetime.now() - datetime.timedelta(minutes=send_minutes))

        assert isinstance(server, smtplib.SMTP)
        i = 0
        for r in self.rule_list:
            i += 1
            # print(type(r),i)
            if (r(self)):
                # server.sendmail(sender, phone, self.get_sms_msg())
                # print(self.last_sent,last_time_threshold)
                if self.last_sent is None or send:
                    send = True
                elif self.last_sent < last_time_threshold:
                    send = True
                    print("SendingAgain {}:".format(send_minutes))
                else:
                    print("Already Send Waiting for {} minute to pass:".format(send_minutes))
        if send:
            for phone in phone_list:
                server.sendmail(sender, phone, self.get_sms_msg())
            print("sending:", self.market)
            self.last_sent = datetime.datetime.now()
        return send

    def get_sms_msg(self):
        return self.msg.format(self.exchange_name,
                               self.symbol.ljust(6,' '),
                               str(self.bid).ljust(10,' '),
                               str(self.sell).ljust(10,' '),
                               str(self.price_yesterday).ljust(10,' '),
                               str(self.price_low_24hr).ljust(10,' '),
                               str(self.price_high_24hr).ljust(10,' '),
                               str(round(self.low_percent, 2)).rjust(5,' '),
                               round(self.high_percent, 2),
                               self.hodl)
