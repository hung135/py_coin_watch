import pprint as pp

class _coin:
    price_now=0
    price_yesterday=0
    price_low_24hr=0
    price_high_24hr=0
    BITTREX_MAP={
         'bid':'Bid',
         'price_high_24hr':'High',
         'price_now':'Last',
         'price_low_24hr':'Low',
         'market':'MarketName',
         'total_buy':'OpenBuyOrders',
         'total_sell':'OpenSellOrders',
         'price_yesterday': 'PrevDay',
         'Volume':'Volume'
    }

    def __init__(self,json,exchange='BITTREX'):
        if type(json) is not dict:
            raise Exception("json must be type dict")
        for key,val in self.BITTREX_MAP.items():
            #print(key)
            #if key=='price_now':
                #print(type(json))
            setattr(self, key, json[val])
                #print("test",self.price_now)


class Exchange:
    msg="{}->{} Price {} Vol {}"

    def get_coin(self,coin):
        pass
    def compare_price(self,hours,market):

        x=self.my_bittrex.get_market_summary(market=market)
        #price_now=x['Bid']
        #price_yesterday=[]
        #low=x['Low']
        json=x['result']
        print(type(json))
        x=_coin(json=json[0])
        #pp.pprint(x['result'])
        print(x.price_now,x.price_yesterday,x.price_low_24hr)
    def __init__(self, api_key=None, secrete_key=None, exchange='BITTREX', market='BTC-USDT'):
        if exchange=='BITTREX':
            from bittrex.bittrex import Bittrex, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            self.my_bittrex = Bittrex(api_key, secrete_key)  # or defaulting to v1.1 as Bittrex(None, None)
            self.my_bittrex.get_markets()
            # print(my_bittrex,dir(my_bittrex))
            self.summary = self.my_bittrex.get_market_summaries()
            # pp.pprint(summary)

            for coin in self.summary['result']:

                if coin['MarketName'].find(market)> 0:

                    self.msg=self.msg.format(exchange,coin['MarketName'],coin['Bid'],coin['Volume'])



