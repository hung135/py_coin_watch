import pprint as pp
from crypto.coin import Coin
from crypto.symbol import SymbolStruct

# Create json to variable mapping for each crypto
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

               }
POLONIEX_MAP = {'market': 'symbol'
    , 'bid': 'highestBid'
    , 'sell': 'lowestAsk'
    , 'price_high_24hr': 'high24hr'
    , 'volume': 'baseVolume'
    , 'price_low_24hr': 'low24hr'
                # , 'price_yesterday': 'prevClosePrice'
    , 'weightedAvgPrice': 'weightedAvgPrice'
                }
YOBIT_MAP = {

    'bid': 'buy'
    , 'sell': 'sell'
    , 'price_high_24hr': 'high'
    , 'volume': 'vol'
    , 'price_low_24hr': 'low'
    # , 'price_yesterday': 'prevClosePrice'

}


class Exchange:
    EX_BINANCE = 'BINANCE'
    EX_BITTREX = 'BITTREX'
    EX_POLONIEX = 'POLONIEX'
    EX_YOBIT = 'YOBIT'
    msg = "{}->{} Price {} Vol {}"
    # market_pattern = None
    # key_api = None
    # key_secret = None
    all_exchange = dict()

    # my_coins = dict()
    # my_coin_market = []
    # exchange_name = None
    # my_hodl = {}
    # all_ticker = []

    # Custom logic for each exchange to get Balance info
    def _get_my_coins(self):
        my_coins = dict()
        if self.exchange_name == 'BINANCE':
            from binance.client import Client as BinanceClient
            x = self.conn.get_account()['balances']
            for asset in x:
                if float(asset['free']) > 10:
                    # print("adding",asset['asset'],type(asset['asset']))
                    my_coins.add(asset['asset'])
                    self.my_hodl[asset['asset']] = asset['free']

            # pp.pprint(x)


        elif self.exchange_name == 'BITTREX':
            pass
        return my_coins

    # Custom Logic for each Exchange to get the connection OBJ
    def _get_conn(self):
        connection_obj = None
        client_obj = None
        if self.exchange_name == 'BINANCE':
            from binance.client import Client as BinanceClient
            client_obj = BinanceClient
            self.market_pattern = "{}BTC"
            self.market_pattern2 = "{0}{1}"
        elif self.exchange_name == 'YOBIT':
            self.market_pattern = "{}_btc"
            self.market_pattern2 = "{0}{1}"
            import YoBit
            client_obj = YoBit.YoBit
        elif self.exchange_name == 'POLONIEX':
            from poloniex.poloniex import Poloniex as PoloniexClient
            # client_obj = PoloniexClient()
            self.market_pattern = "BTC_{}"
            self.market_pattern2 = "{1}_{0}"
            connection_obj = PoloniexClient()
        elif self.exchange_name == 'BITTREX':
            from bittrex import Bittrex as BittrexClient, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            client_obj = BittrexClient
            self.market_pattern = "BTC-{}"
            self.market_pattern2 = "{1}-{0}"

        if client_obj is not None and connection_obj is None:
            connection_obj = client_obj(self.key_api, self.key_secret)

        return connection_obj

    def get_all_ticker(self):

        # print("getcoindata",Coin.market,Coin.exchange_name)
        if self.exchange_name == 'YOBIT':
            import YoBit
            assert isinstance(self.conn, YoBit.YoBit)
            json = self.conn.info()
            for m in json['pairs']:
                self.all_ticker.append(m)

        if self.exchange_name == 'POLONIEX':
            from poloniex import Poloniex
            assert isinstance(self.conn, Poloniex)
            json = dict(self.conn.returnTicker())
            for m in json:
                self.all_ticker.append(m)

        if self.exchange_name == 'BINANCE':
            from binance.client import Client as BinanceClient
            assert isinstance(self.conn, BinanceClient)
            json = self.conn.get_all_tickers()
            for m in json:
                self.all_ticker.append(m['symbol'])
        if self.exchange_name == 'BITTREX':
            from bittrex import Bittrex, API_V2_0
            assert isinstance(self.conn, Bittrex)
            summary = self.conn.get_markets()

            for m in summary['result']:
                self.all_ticker.append(m['MarketName'])

    # Custom lock for each exchange to get pricing JSON data
    def get_coin_data_json(self, coin):
        json = {}
        assert isinstance(coin, Coin)
        # print("getcoindata",Coin.market,Coin.exchange_name)
        if self.exchange_name == 'YOBIT':
            self.exchange_map = YOBIT_MAP
            import YoBit
            assert isinstance(self.conn, YoBit.YoBit)
            json = self.conn.ticker(coin.market)[coin.market]

        if self.exchange_name == 'POLONIEX':
            self.exchange_map = POLONIEX_MAP
            from poloniex import Poloniex
            assert isinstance(self.conn, Poloniex)
            json = dict(self.conn.returnTicker()[coin.market])

        if self.exchange_name == 'BINANCE':
            try:

                json = self.conn.get_ticker(symbol=coin.market)
            except Exception as e:
                print("Error getting coin data:{}".format(coin.market))
            self.exchange_map = BINANCE_MAP

        if self.exchange_name == 'BITTREX':
            self.exchange_map = BITTREX_MAP
            from bittrex import Bittrex, API_V2_0
            assert isinstance(self.conn, Bittrex)

            summary = self.conn.get_market_summary(coin.market)

            for m in summary['result']:

                if m['MarketName'] == coin.market:
                    json = m

        return json

    # returns object so we can refresh the data
    def create_coin_market(self):
        self.my_coin_market = dict()
        print(self.exchange_name, self.my_coin_market)
        for symbol_maket, symbol in self.my_coins.items():
            #hodl = self.my_hodl.get(symbol, 0)
            hodl=0
            self.my_coin_market[symbol_maket] = (
                # Coin(symbol_maket, exchange_obj=self, symbol=symbol, hodl=hodl))
                Coin(symbol[0],symbol[1], self,hodl))
        for symbol_maket, symbol in self.all_exchange.items():
            # print("inside",symbol,type(symbol),self.market_pattern2)
            self.my_coin_market[self.market_pattern2.format(symbol[0], symbol[1])] = (
                Coin(symbol[0], symbol[1], exchange_obj=self,hodl=0))

            # print(self.exchange_name, self.my_coin_market)
        return self.my_coin_market

    def add_coin_symbolV2(self, coin_struct):

        if (coin_struct.all_exchange):
            self.all_exchange[self.keytemplate.format(coin_struct.symbol, coin_struct.basemarket)] = list(
                [coin_struct.symbol, coin_struct.basemarket])

        else:
            assert isinstance(coin_struct, SymbolStruct)
            # market_symbol = self.market_pattern2.format(coin_struct.symbol, coin_struct.basemarket)
            self.my_coins[self.keytemplate.format(coin_struct.symbol, coin_struct.basemarket)] = list(
                [coin_struct.symbol, coin_struct.basemarket])

    def add_coin_symbol(self, coin_symbol, basemarket,all_exchange=False):
        if (all_exchange):
            self.all_exchange[self.keytemplate.format(coin_symbol, basemarket)] = list(
                [coin_symbol,basemarket])
        else:
            self.my_coins[self.keytemplate.format(coin_symbol, basemarket)] = list(
                [coin_symbol,basemarket])

    # initial all instance variables
    def __init__(self,  api_key=None, secret_key=None, exchange='BITTREX'):
        # We have to initalize all instance variable here
        self.keytemplate = "{}-{}"
        self.market_pattern = "{0}-{1}"
        self.my_coin_market = []
        self.my_hodl = {}
        self.all_ticker = []
        self.my_coins = dict()
        self.key_api = api_key
        self.key_secret = secret_key
        self.exchange_name = exchange
        self.conn = self._get_conn()

        # self.my_coins = self._get_my_coins()
        # self.get_all_ticker()
        print("Connected To:", exchange, self.all_exchange)
