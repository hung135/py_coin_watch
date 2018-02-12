import pprint as pp
from crypto.coin import Coin

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
    market_pattern = None
    key_api = None
    key_secret = None
    msg = "{}->{} Price {} Vol {}"
    my_coins = set()
    my_coin_market = []
    exchange_name = None
    my_hodl = {}
    all_ticker = []

    # Custom logic for each exchange to get Balance info
    def _get_my_coins(self):
        my_coins = set()
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

        elif self.exchange_name == 'YOBIT':
            self.market_pattern = "{}_btc"

            import YoBit
            client_obj = YoBit.YoBit
        elif self.exchange_name == 'POLONIEX':
            from poloniex.poloniex import Poloniex as PoloniexClient
            # client_obj = PoloniexClient()
            self.market_pattern = "BTC_{}"
            connection_obj = PoloniexClient()
        elif self.exchange_name == 'BITTREX':
            from bittrex import Bittrex as BittrexClient, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            client_obj = BittrexClient
            self.market_pattern = "BTC-{}"
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

    def create_coin_market(self):
        self.my_coin_market = []
        for symbol in self.my_coins:
            hodl = self.my_hodl.get(symbol, 0)
            self.my_coin_market.append(
                Coin(self.market_pattern.format(symbol), exchange_obj=self, symbol=symbol, hodl=hodl))
        return self.my_coin_market

    def add_coin_symbol(self, coin_symbol, hodl=0):
        # print(type(self.my_coins))
        self.my_coins.add(coin_symbol)
        self.my_coins = set(self.my_coins)
        if (self.my_hodl.get(coin_symbol, 0)) == 0:
            # print(self.my_hodl)
            self.my_hodl[coin_symbol] = hodl

    def __init__(self, api_key=None, secret_key=None, exchange='BITTREX'):
        self.key_api = api_key
        self.key_secret = secret_key
        self.exchange_name = exchange
        self.conn = self._get_conn()
        self.my_coins = self._get_my_coins()
        #self.get_all_ticker()
