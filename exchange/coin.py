import exchange
class Coin:
    msg = "{}->{} \nB{} \nA{} \nYest {} \nlow {} \nhigh {}\n L{}% H{}%"
    bid = None
    sell = None
    last = None
    market = None
    exchange_name = None
    exchange_conn = None
    low_percent=100
    high_percent=0
    price_yesterday = 0
    price_low_24hr = 0
    price_high_24hr = 0
    BITTREX_MAP = {
        'bid': 'Bid',
        'sell': 'Sell',
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

    def __init__(self, coin_market, exchange_obj):
        self.market=coin_market
        assert isinstance(exchange_obj, exchange.Exchange)
        self.exchange_name=exchange_obj.exchange_name
        self.exchange_conn=exchange_obj
        self.refresh()

    def fill_data(self, json, exchange_map, ex_name):
        self.exchange = ex_name
        if type(json) is not dict:
            raise Exception("json must be type dict")
        if type(exchange_map) is not dict:
            raise Exception("exchange_map must be type dict")
        # looks through json and pulls fields that matches the mapping and set the instance variable
        for key, val in exchange_map.items():
            value = json.get(val, 0)
            if value != 0:
                setattr(self, key, value)
        self.low_percent=float(exchange.Rule.check_24hr_low(self))
        self.high_percent=float(exchange.Rule.check_24hr_high(self))

    def fill_data2(self, json):

        if type(json) is not dict:
            raise Exception("json must be type dict")
        if type(self.BINANCE_MAP) is not dict:
            raise Exception("exchange_map must be type dict")
        # looks through json and pulls fields that matches the mapping and set the instance variable
        for key, val in self.BINANCE_MAP.items():
            value = json.get(val, 0)
            if value != 0:
                setattr(self, key, value)
        self.low_percent=float(exchange.Rule.check_24hr_low(self))
        self.high_percent=float(exchange.Rule.check_24hr_high(self))

    def refresh(self):

        self.fill_data2(self.exchange_conn.get_coin_data_json(self))


    def get_sms_msg(self):
        return self.msg.format(self.exchange_name
                               , self.market
                               , self.bid,
                               self.sell,
                               self.price_yesterday,
                               self.price_low_24hr,
                               self.price_high_24hr,
                               round(self.low_percent,2),
                               round(self.high_percent,2))


