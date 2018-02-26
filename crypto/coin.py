import datetime
import time
import pprint as pp
import smtplib

import crypto
import arrow

class Coin:
    msg = "{}->{}\nB{}\nA{} \nPrev {}\nL {}\nH {}\nL{}% H{}%\nQTY {}\nNEWS{}"
    send_buffer = dict()
    last_sent = dict()
    rule_list = set()
    rule_threshhold = .45

    def __init__(self, symbol,basemarket, exchange_obj,hodl=0):
        assert isinstance(exchange_obj, crypto.Exchange)

        self.bid = 0
        self.sell = 0
        self.last = 0
        self.error_msg = None
        self.name = symbol #Common nname
        self.symbol = symbol
        self.basemarket = basemarket
        self.market = exchange_obj.market_pattern2.format(self.symbol, self.basemarket)

        self.exchange_name = exchange_obj.exchange_name
        self.exchange_conn = exchange_obj
        self.low_percent = 100
        self.high_percent = 0
        self.price_yesterday = 0
        self.price_low_24hr = 0
        self.price_high_24hr = 0
        self.hodl = hodl
        self.rule_list.add(crypto.Rule.check_24hr_low)
        self.rule_list.add(crypto.Rule.check_24hr_high)
        self.refresh()
        self.news_feed=None

    def fill_data(self, json):
        assert isinstance(json,dict)
        assert isinstance(self.exchange_conn.exchange_map,dict)

        # looks through json and pulls fields that matches the mapping and set the instance variable

        for key, val in self.exchange_conn.exchange_map.items():

            value = json.get(val, 0)
            if value != 0:

                setattr(self, key, value)
        self.low_percent = float(crypto.Rule.get_delta_24hr_low(self))
        self.high_percent = float(crypto.Rule.get_delta_24hr_high(self))
    def set_news(self,news_feed=None):
        if news_feed is not None:
            self.news_feed=news_feed

    def refresh(self):
        # try:
        self.fill_data(
            self.exchange_conn.get_coin_data_json(self))  # except Exception as e:  #   print("Error Filling Data:", e)

    def fill_send_buffer(self, delay_minutes=20):
        for r in self.rule_list:
            if (r(self)):
                self.send_buffer[self.symbol + self.basemarket] = list(
                    [datetime.datetime.now(), self.get_sms_msg(), delay_minutes])

    def send_sms(self, server, sender, phone_list, send_minutes=30,news = None):
        send = False
        assert isinstance(phone_list, list)

        last_time_threshold = (datetime.datetime.now() - datetime.timedelta(minutes=send_minutes))

        # assert isinstance(server, smtplib.SMTP)
        i = 0
        for r in self.rule_list:
            i += 1
            # print(type(r),i)
            if (r(self)):
                # server.sendmail(sender, phone, self.get_sms_msg())
                # print(self.last_sent,last_time_threshold)
                #find the record of the last time sent
                last_sent_dict=self.last_sent.get(self.symbol+self.basemarket, None)
                price_delta_low=0
                price_delta_low = 0
                if last_sent_dict:
                    price_delta_low=(float(last_sent_dict["sent_low"])) - float(self.bid)
                    price_delta_high=(float(last_sent_dict["sent_high"])) - float(self.sell)

                #print(last_sent_dict,"---")
                if last_sent_dict is None or send:
                    send = True

                elif last_sent_dict["sent_time"] < last_time_threshold:
                    send = True
                    print("SendingAgain {}:".format(send_minutes))
                else:
                    print("Already Send Waiting for {} minute to pass:".format(send_minutes))
        if send:
            from twilio.rest import Client
            assert isinstance(server, Client)
            self.last_sent[self.symbol+self.basemarket] = {"sent_time":datetime.datetime.now()
                                                           ,"sent_price":self.bid
                                                           ,"sent_low":self.price_low_24hr
                                                           ,"sent_high":self.price_high_24hr}
            for phone in phone_list:
                # server.sendmail(sender, phone, self.get_sms_msg())
                message = server.messages.create(
                    to=phone_list,
                    from_=sender,
                    body=self.get_sms_msg() + "\n" + time.ctime())

            #print("sending:", self.market)
            # self.last_sent = datetime.datetime.now()
        return send

    @staticmethod
    def get_table_header():
        template = "{}{}{}{}{}{}{}{}{}{}{}{}{}"
        txt = template.format(
            str("EXCHANGE").ljust(10, ' '),
            str("COIN").ljust(10, ' '),
            str("BUY").ljust(12, ' '),
            str("ASK").ljust(12, ' '),
            str("PREV").ljust(12, ' '),
            str("LOW").ljust(12, ' '),
            str("HIGH").ljust(12, ' '),
            str("%FromLOW").ljust(10, ' '),
            str("%FromHIGH").ljust(10, ' '),
            str("BTC").ljust(10, ' '),
            str("HOLD").ljust(10, ' '),
            str("ERRMSG").ljust(10, ' '),
            str("News").ljust(10, ' ')
        )
        return txt

    def get_formatted_table_row(self):
        template = "{}{}{}{}{}{}{}{}{}{}{}{}{}"
        if self.basemarket=='USDT':
            sat = 1
            buyprice="$"+str(round(float(self.bid) * sat)).ljust(12, ' ')
        else:
            sat = 100000000
            buyprice=str(round(float(self.bid) * sat)).ljust(12, ' ')
        btc = 0.0
        try:
            btc = round(float(self.hodl) * float(self.bid), 3)
        except:
            btc = 0.0
        news=''
        if self.news_feed is not None:
            for y in self.news_feed:
                data_date=arrow.get(y['data_date'], 'D MMMM YYYY').format('MM/DD')
                news=news+"-" +data_date +":"+ y['data_title']
        txt = template.format(
            str(self.exchange_name).ljust(10, ' '),
            str("{}-{}".format(self.symbol,self.basemarket)).ljust(10, ' '),
            buyprice,
            str(round(float(self.sell) * sat)).ljust(12, ' '),

            # str(self.sell).ljust(12, ' '),
            str(round(float(self.price_yesterday) * sat)).ljust(12, ' '),
            # str(self.price_yesterday).ljust(12, ' '),
            # str(self.price_low_24hr).ljust(12, ' '),
            str(round(float(self.price_low_24hr) * sat)).ljust(12, ' '),

            # str(self.price_high_24hr).ljust(12, ' '),
            str(round(float(self.price_high_24hr) * sat)).ljust(12, ' '),
            str(round(self.low_percent, 2)).ljust(10, ' '),

            str(round(self.high_percent, 2)).ljust(10, ' '),
            str(btc).ljust(7, ' '),
            str(self.hodl).ljust(10, ' '),
            self.error_msg,
            news
        )
        return txt

    def get_sms_msg(self):
        news=''
        if self.news_feed is not None:
            for y in self.news_feed:
                data_date=arrow.get(y['data_date'], 'D MMMM YYYY').format('MM/DD')
                news=news+"-" +data_date +":"+ y['data_title']
        return self.msg.format(self.exchange_name,
                               self.market.ljust(6, ' '),
                               str(self.bid).ljust(10, ' '),
                               str(self.sell).ljust(10, ' '),
                               str(self.price_yesterday).ljust(10, ' '),
                               str(self.price_low_24hr).ljust(10, ' '),
                               str(self.price_high_24hr).ljust(10, ' '),
                               str(round(self.low_percent, 2)).rjust(5, ' '),
                               round(self.high_percent, 2),
                               self.hodl,
                               news)
