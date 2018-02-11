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
    , 'weightedAvgPrice': 'weightedAvgPrice'
               }


class Exchange:
    EX_BINANCE = 'BINANCE'
    EX_BITTREX = 'BITTREX'
    EX_POLINEX = 'POLINEX'
    market_pattern = None
    key_api = None
    key_secret = None
    msg = "{}->{} Price {} Vol {}"
    my_coins = set()
    my_coin_market = []
    exchange_name = None

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
                # self.msg = self.msg.format(self.crypto, coin['MarketName'], coin['Bid'], coin['Volume'])

    def _do_binance(self, api_key, secrete_key, market):
        from binance.client import Client
        client = Client(api_key, secrete_key)
        price = client.get_ticker(symbol=market)
        self.coin = _coin(json=price, exchange_map=_coin.BINANCE_MAP, ex_name='BINANCE')

    def _get_my_coins(self):
        my_coins = set()
        if self.exchange_name == 'BINANCE':
            from binance.client import Client as BinanceClient
            x = self.conn.get_account()['balances']
            for asset in x:
                if float(asset['free']) > 1:
                    # print("adding",asset['asset'],type(asset['asset']))
                    my_coins.add(asset['asset'])

            # pp.pprint(x)


        elif self.exchange_name == 'BITTREX':
            pass
        return my_coins

    def _get_conn(self):
        connection_obj = None
        client_obj = None
        if self.exchange_name == 'BINANCE':
            from binance.client import Client as BinanceClient
            client_obj = BinanceClient
            self.market_pattern = "{}BTC"
        elif self.exchange_name == 'BITTREX':
            from bittrex.bittrex import Bittrex as BittrexClient, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            client_obj = BittrexClient
            self.market_pattern = "BTC-{}"
        if client_obj is not None:
            connection_obj = client_obj(self.key_api, self.key_secret)

        return connection_obj

    def add_coin_symbol(self, coin_symbol):
        # print(type(self.my_coins))
        self.my_coins.add(coin_symbol)
        self.my_coins = set(self.my_coins)

    def get_coin_data_json(self, Coin):
        json = {}
        # print("getcoindata",Coin.market,Coin.exchange_name)
        if Coin.exchange_name == 'BINANCE':
            json = self.conn.get_ticker(symbol=Coin.market)
            self.exchange_map = BINANCE_MAP
        if Coin.exchange_name == 'BITTREX':
            self.exchange_map = BITTREX_MAP

            summary = self.conn.get_market_summaries()

            for coin in summary['result']:
                if coin['MarketName'] == Coin.market:
                    json = coin
                    # pp.pprint(coin)

        return json

    def create_coin_market(self):
        self.my_coin_market = []
        for a in self.my_coins:
            self.my_coin_market.append(Coin(self.market_pattern.format(a), exchange_obj=self))
        return self.my_coin_market

    def __init__(self, api_key=None, secret_key=None, exchange='BITTREX'):
        self.key_api = api_key
        self.key_secret = secret_key
        self.exchange_name = exchange
        self.conn = self._get_conn()
        self.my_coins = self._get_my_coins()