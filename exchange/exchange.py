import pprint as pp

# Create json to variable mapping for each exchange
BITTREX_MAP = {
    'bid': 'Bid',
    'sell': 'Ask',
    'price_high_24hr': 'High',
    'last': 'Last',
    'price_low_24hr': 'Low',
    'market': 'MarketName',
    'total_buy': 'OpenBuyOrders',
    'total_sell': 'OpenSellOrders',
    'price_yesterday': 'PrevDay',
    'volume': 'Volume'
}
BINANCE_MAP = {'market': 'symbol'
    , 'bid': 'bidPrice'
    , 'sell': 'askPrice'
    , 'price_high_24hr': 'highPrice'
    , 'volume': 'volume'
    , 'price_low_24hr': 'lowPrice'
    , 'price_yesterday': 'prevClosePrice'
    , 'weightedAvgPrice': 'weightedAvgPrice'
               }

class _coin:
    msg = "{}->{} \nB{} \nA{} \nYest {} \nlow {} \nhigh {}\n L{}% H{}%"
    bid = None
    sell = None
    last = None
    market = None
    exchange_name = None
    low_percent = 100
    high_percent = 0
    price_yesterday = 0
    price_low_24hr = 0
    price_high_24hr = 0


    def __init__(self, json, exchange_map, ex_name):
        self.exchange_name = ex_name
        if type(json) is not dict:
            raise Exception("json must be type dict")
        if type(exchange_map) is not dict:
            raise Exception("exchange_map must be type dict")
        # looks through json and pulls fields that matches the mapping and set the instance variable
        for key, val in exchange_map.items():
            value = json.get(val, 0)
            if value != 0:
                setattr(self, key, value)
        self.low_percent = float(exchange_name.Rule.check_24hr_low(self))
        self.high_percent = float(exchange_name.Rule.check_24hr_high(self))

    def refresh(self, exchange):
        pass

    def get_sms_msg(self):
        return self.msg.format(self.exchange_name
                               , self.market
                               , self.bid,
                               self.sell,
                               self.price_yesterday,
                               self.price_low_24hr,
                               self.price_high_24hr,
                               round(self.low_percent, 2),
                               round(self.high_percent, 2))


class Exchange:
    EX_BINANCE = 'BINANCE'
    EX_BITTREX = 'BITTREX'
    EX_POLINEX = 'POLINEX'
    key_api = None
    key_secret = None
    msg = "{}->{} Price {} Vol {}"
    coin = None
    exchange_name = None
    def get_coin(self, coin):
        pass

    def compare_price(self, hours, market):
        pass
        # x=self.my_bittrex.get_market_summary(market=market)
        # price_now=x['Bid']
        # price_yesterday=[]
        # low=x['Low']
        # json=x['result']
        # print(type(json))
        # x=_coin(json=json[0])
        # pp.pprint(x['result'])
        # print(x.price_now,x.price_yesterday,x.price_low_24hr)

    def _do_bittrex(self, api_key, secrete_key, market):
        from bittrex.bittrex import Bittrex, API_V2_0

        # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
        self.my_bittrex = Bittrex(api_key, secrete_key)  # or defaulting to v1.1 as Bittrex(None, None)
        self.my_bittrex.get_markets()
        # print(my_bittrex,dir(my_bittrex))
        self.summary = self.my_bittrex.get_market_summaries()
        # pp.pprint(summary)

        for coin in self.summary['result']:
            if coin['MarketName'].find(market) > 0:
                self.coin = _coin(json=coin, exchange_map=_coin.BINANCE_MAP, ex_name='BITTREX')
                # self.msg = self.msg.format(self.exchange, coin['MarketName'], coin['Bid'], coin['Volume'])

    def _do_binance(self, api_key, secrete_key, market):
        from binance.client import Client
        client = Client(api_key, secrete_key)
        price = client.get_ticker(symbol=market)
        self.coin = _coin(json=price, exchange_map=_coin.BINANCE_MAP, ex_name='BINANCE')

    def get_conn(self, exchange):
        connection_obj = None
        client_obj = None
        if exchange == 'BINANCE':
            from binance.client import Client
            client_obj = Client
        elif exchange == 'BITTREX':
            from bittrex.bittrex import Bittrex, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            client_obj = Bittrex

        if client_obj is not None:
            connection_obj = client_obj(self.key_api, self.key_secret)

        return connection_obj

    def get_coin_data_json(self,Coin):
        json = {}
        #print("getcoindata",Coin.market,Coin.exchange_name)
        if Coin.exchange_name=='BINANCE':
            json = self.conn.get_ticker(symbol=Coin.market)
            self.exchange_map=BINANCE_MAP
        if Coin.exchange_name=='BITTREX':
            self.exchange_map=BITTREX_MAP

            summary=self.conn.get_market_summaries()

            for coin in summary['result']:
                if coin['MarketName']==Coin.market:
                    json=coin
                    #pp.pprint(coin)


        return json


    def __init__(self, api_key=None, secrete_key=None, exchange='BITTREX'):
        self.conn = self.get_conn(exchange)
        self.exchange_name=exchange

    def do_nothing(self, api_key=None, secrete_key=None, exchange='BITTREX', market='BTC-USDT'):
        self.exchange = exchange
        if exchange == 'BITTREX':
            self._do_bittrex(api_key, secrete_key, market)
        if exchange == 'BINANCE':
            self._do_binance(api_key, secrete_key, market)
