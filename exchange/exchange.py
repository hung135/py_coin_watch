import pprint as pp


class _coin:
    bid = None
    sell = None
    last = None
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
        , 'bid': 'Bid'
        , 'sell': 'Sell'
        , 'bid': 'price'
        , 'price_high_24hr': 'high'
        , 'volume': 'volume'
        , 'price_low_24hr': 'low'
        , 'price_yesterday': 'prevClose'
                   }

    def __init__(self, json, exchange_map):
        if type(json) is not dict:
            raise Exception("json must be type dict")
        if type(exchange_map) is not dict:
            raise Exception("exchange_map must be type dict")
        # looks through json and pulls fields that matches the mapping and set the instance variable
        for key, val in exchange_map.items():
            value = json.get(val, 0)
            if value != 0:
                setattr(self, key, value)

    def print_price(self):
        print(self.bid,
              self.sell,
              self.price_yesterday,
              self.price_low_24hr,
              self.price_high_24hr)


class Exchange:
    msg = "{}->{} Price {} Vol {}"
    coin = None

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
                self.msg = self.msg.format(self.exchange, coin['MarketName'], coin['Bid'], coin['Volume'])

    def _do_binance(self, api_key, secrete_key, market):
        from binance.client import Client
        client = Client(api_key, secrete_key)

        # get market depth
        depth = client.get_order_book(symbol=market).get('bids', "")
        pp.pprint(depth[0])
        # place market buy order
        """order = client.create_order(
            symbol=market,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=100)"""
        products = client.get_products()
        # get all symbol prices
        # prices = client.get_all_tickers()
        # print(prices)
        for coin in products['data']:
            if coin['symbol'] == market:
                # pp.pprint(coin)
                self.coin = _coin(json=coin, exchange_map=_coin.BINANCE_MAP)

    def __init__(self, api_key=None, secrete_key=None, exchange='BITTREX', market='BTC-USDT'):
        self.exchange = exchange
        if exchange == 'BITTREX':
            self._do_bittrex(api_key, secrete_key, market)
        if exchange == 'BINANCE':
            self._do_binance(api_key, secrete_key, market)
