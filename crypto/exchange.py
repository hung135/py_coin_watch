import pprint as pp
from crypto.coin import Coin
from crypto.symbol import SymbolStruct

# Create json to variable mapping for each crypto
BITTREX_MAP = {'bid': 'Bid', 'sell': 'Ask', 'price_high_24hr': 'High', 'last': 'Last', 'price_low_24hr': 'Low',
               'market': 'MarketName', 'total_buy': 'OpenBuyOrders', 'total_sell': 'OpenSellOrders',
               'price_yesterday': 'PrevDay', 'volume': 'Volume', 'error_msg': 'error_msg'

               }
BINANCE_MAP = {'market': 'symbol', 'bid': 'bidPrice', 'sell': 'askPrice', 'price_high_24hr': 'highPrice',
               'volume': 'volume', 'price_low_24hr': 'lowPrice', 'price_yesterday': 'prevClosePrice',
               'error_msg': 'error_msg'

               }
POLONIEX_MAP = {'market': 'symbol', 'bid': 'highestBid', 'sell': 'lowestAsk', 'price_high_24hr': 'high24hr',
                'volume': 'baseVolume', 'price_low_24hr': 'low24hr'  # , 'price_yesterday': 'prevClosePrice'
    , 'weightedAvgPrice': 'weightedAvgPrice'
    , 'error_msg': 'error_msg'}
YOBIT_MAP = {

    'bid': 'buy', 'sell': 'sell', 'price_high_24hr': 'high', 'volume': 'vol', 'price_low_24hr': 'low', 'error_msg': 'error_msg'
    # , 'price_yesterday': 'prevClosePrice'

}
CRYPTOPIA_MAP = {

    'bid': 'BidPrice', 'sell': 'AskPrice', 'price_high_24hr': 'High', 'volume': 'Volume', 'price_low_24hr': 'Low', 'error_msg': 'error_msg'
     , 'price_yesterday': 'Close'
}

class Exchange:
    EX_BINANCE = 'BINANCE'
    EX_BITTREX = 'BITTREX'
    EX_POLONIEX = 'POLONIEX'
    EX_YOBIT = 'YOBIT'
    EX_CRYPTOPIA = 'CRYPTOPIA'
    COIN_NO_FOUND = 'COIN NOT FOUND'
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
        elif self.exchange_name == 'CRYPTOPIA':
            self.market_pattern = "{}/BTC"
            self.market_pattern2 = "{0}/{1}"
            from crypto import Api as CryptopiaClient
            client_obj = CryptopiaClient
        elif self.exchange_name == 'YOBIT':
            self.market_pattern = "{}_btc"
            self.market_pattern2 = "{0}_{1}"
            import YoBit
            client_obj = YoBit.YoBit
        elif self.exchange_name == 'POLONIEX':
            from poloniex.poloniex import Poloniex as PoloniexClient
            # client_obj = PoloniexClient()
            self.market_pattern = "BTC_{}"
            self.market_pattern2 = "{1}_{0}"
            connection_obj = PoloniexClient()
        elif self.exchange_name == 'BITTREX':
            from bittrex import Bittrex as BittrexClient
            #, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            client_obj = BittrexClient
            self.market_pattern = "BTC-{}"
            self.market_pattern2 = "{1}-{0}"

        if client_obj is not None and connection_obj is None:
            connection_obj = client_obj(self.key_api, self.key_secret)

        return connection_obj

    def get_all_ticker(self):
        if self.exchange_name == self.EX_CRYPTOPIA:
            from crypto import Api
            assert isinstance(self.conn, Api)
            json = self.conn.get_tradepairs()[0]
            # print(str(json)[:200])
            import time

            for val in json:
                # print(str(val))
                coin = {"symbol": val['Symbol'], "name": val['BaseSymbol'], "market": val['Label'], "price": 0}
                self.all_ticker[val['Label']] = coin

        if self.exchange_name == 'YOBIT':
            import YoBit
            assert isinstance(self.conn, YoBit.YoBit)
            json = self.conn.info()['pairs']

            for key, val in json.items():
                # print(str(val))
                coin = {"symbol": key, "name": key, "market": key, "price": 0}
                self.all_ticker[key] = coin

        if self.exchange_name == 'POLONIEX':
            from poloniex import Poloniex
            assert isinstance(self.conn, Poloniex)
            json = dict(self.conn.returnTicker())
            for m in json.items():
                self.all_ticker.append(m)

        if self.exchange_name == self.EX_BINANCE:

            dict_set = set()
            from binance.client import Client as BinanceClient
            assert isinstance(self.conn, BinanceClient)
            json = self.conn.get_products()

            for val in json['data']:
                # print(val)
                coin = {"symbol": val['baseAsset'], "name": val['baseAssetName'], "market": val['symbol'], "price": 0}

                self.all_ticker[val['symbol']] = coin

        if self.exchange_name == self.EX_BITTREX:
            from bittrex import Bittrex #, API_V2_0
            assert isinstance(self.conn, Bittrex)
            summary = self.conn.get_markets()

            for m in summary['result']:
                self.all_ticker.append(m['MarketName'])
        return self.all_ticker
    # Custom lock for each exchange to get pricing JSON data
    def get_coin_data_json(self, coin):
        json = {}
        assert isinstance(coin, Coin)
        # print("getcoindata",Coin.market,Coin.exchange_name)
        if self.exchange_name == 'CRYPTOPIA':
            self.exchange_map = CRYPTOPIA_MAP
            from crypto import Api
            assert isinstance(self.conn, Api)
            #if self.mulptile_pairs_json is None:
            json ,error = self.conn.get_markets()
            #self.mulptile_pairs_json=json

            found=False
            if error is None and json is not None:
                for x in json:
                    if(x['Label']==coin.market):
                        json=dict(x)
                        found=True
                        break
                if not found:
                    json = dict({'error_msg': self.COIN_NO_FOUND})
            else:
                json = dict({'error_msg': error})

        if self.exchange_name == 'YOBIT':
            self.exchange_map = YOBIT_MAP
            import YoBit
            assert isinstance(self.conn, YoBit.YoBit)
            try:
                json = self.conn.ticker(coin.market)
            except:
                json = {'success',0}
            assert isinstance(json, dict)
            if json.get('success', 1) == 1:
                json = json[coin.market.lower()]

            else:
                json = dict({'error_msg': self.COIN_NO_FOUND})


        if self.exchange_name == 'POLONIEX':
            self.exchange_map = POLONIEX_MAP
            from poloniex import Poloniex
            assert isinstance(self.conn, Poloniex)
            try:
                json = dict(self.conn.returnTicker())
                if json.get(coin.market, 0) != 0:
                    json = dict(json.get(coin.market))
                else:
                    json = dict({'error_msg': self.COIN_NO_FOUND})
            except Exception as e:
                json = dict({'error_msg': self.COIN_NO_FOUND})
            # print(json,coin.market)


        if self.exchange_name == 'BINANCE':
            self.exchange_map = BINANCE_MAP
            try:
                from binance.client import Client
                assert isinstance(self.conn, Client)
                json = self.conn.get_ticker(symbol=coin.market)
            except Exception as e:
                json = dict({'error_msg': self.COIN_NO_FOUND})



        if self.exchange_name == 'BITTREX':
            self.exchange_map = BITTREX_MAP
            from bittrex.bittrex import Bittrex
            assert isinstance(self.conn, Bittrex)
            #print(self.conn)
            summary = self.conn.get_market_summary(coin.market)
            #print(summary,coin.market)
            if summary.get('success', False) == True:
                for m in summary.get('result', {}):
                    if m.get('MarketName', None) == coin.market:
                        json = m
            else:
                json = dict({'error_msg': self.COIN_NO_FOUND})

        return json

    # returns object so we can refresh the data
    def create_coin_market(self):
        self.my_coin_market = dict()

        for symbol_maket, symbol in self.my_coins.items():
            # hodl = self.my_hodl.get(symbol, 0)
            hodl = 0
            self.my_coin_market[symbol_maket] = (  # Coin(symbol_maket, exchange_obj=self, symbol=symbol, hodl=hodl))
                Coin(symbol[0], symbol[1], self, hodl))
        for symbol_maket, symbol in self.all_exchange.items():
            self.my_coin_market[self.market_pattern2.format(symbol[0], symbol[1])] = (
                Coin(symbol[0], symbol[1], exchange_obj=self, hodl=0))

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

    def add_coin_symbol(self, coin_symbol, basemarket, all_exchange=False):
        if (all_exchange):
            self.all_exchange[self.keytemplate.format(coin_symbol, basemarket)] = list([coin_symbol, basemarket])
        else:
            self.my_coins[self.keytemplate.format(coin_symbol, basemarket)] = list([coin_symbol, basemarket])

    # initial all instance variables
    def __init__(self, api_key=None, secret_key=None, exchange='BITTREX'):
        # We have to initalize all instance variable here
        self.keytemplate = "{}-{}"
        self.market_pattern = "{0}-{1}"
        self.my_coin_market = []
        self.my_hodl = {}
        self.all_ticker = dict()  #symbol,coin name, marketsymbol
        self.my_coins = dict()
        self.key_api = api_key
        self.key_secret = secret_key
        self.exchange_name = exchange
        self.conn = self._get_conn()
        self.mulptile_pairs_json=None # will be used to store exchanges that don't give json for a single coin
        # self.my_coins = self._get_my_coins()
        # self.get_all_ticker()
        print("Connected To:", exchange, self.all_exchange)
