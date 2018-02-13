from crypto import Coin


class Rule():
    to_do_list = None

    @staticmethod
    def get_delta_24hr_low(coin, threshold_percent=.5):
        # print(Coin.get_sms_msg())

        assert isinstance(coin, Coin)
        avg_price = (float(coin.sell))
        price = float(coin.price_low_24hr)
        if price == 0:
            return 0
        delta = abs(avg_price - float(price))
        low_delta_sat = delta * 100000000
        delta_percent = (delta / price) * 100

        return delta_percent

    @staticmethod
    def get_delta_24hr_high(coin, threshold_percent=.5):

        avg_price = (float(coin.bid))
        price = float(coin.price_high_24hr)
        if price == 0:
            return 0
        delta = abs(avg_price - float(price))
        low_delta_sat = delta * 100000000
        delta_percent = (delta / price) * 100

        return delta_percent

    # ##################################################################
    @staticmethod
    def check_24hr_low(coin, threshold_percent=.5):
        assert isinstance(coin, Coin)
        send = False
        assert isinstance(coin, Coin)
        if float(coin.low_percent) < threshold_percent:
            send = True
        # print(coin.market, send,'low',float(coin.low_percent),threshold_percent)
        return send

    @staticmethod
    def check_24hr_high(coin, threshold_percent=.5):
        assert isinstance(coin, Coin)
        send = False
        assert isinstance(coin, Coin)
        if float(coin.high_percent) < threshold_percent:
            send = True
        # print(coin.market,send,'High',float(coin.high_percent),threshold_percent)
        return send
