import pprint as pp


class Exchange:
    msg="{}->{} Price {} Vol {}"

    def get_coin(self,coin):

        return "FUCKU"
    def __init__(self,api_key=None,secrete_key=None,exchange='BITTREX',coin_str='BTC-USDT'):
        if exchange=='BITTREX':
            from bittrex.bittrex import Bittrex, API_V2_0
            # my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
            my_bittrex = Bittrex(api_key, secrete_key)  # or defaulting to v1.1 as Bittrex(None, None)
            my_bittrex.get_markets()
            # print(my_bittrex,dir(my_bittrex))
            summary = my_bittrex.get_market_summaries()
            # pp.pprint(summary)

            for coin in summary['result']:

                if coin['MarketName'].find(coin_str )> 0:
                    print(coin_str)
                    self.msg=self.msg.format(exchange,coin['MarketName'],coin['Bid'],coin['Volume'])



