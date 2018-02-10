from exchange import Coin
class Rule:
    to_do_list=None
    
    def check_24hr_low(Coin, threshold_percent=.5):
        #print(Coin.get_sms_msg())
        avg_price=(float(Coin.sell))
        price=float(Coin.price_low_24hr)

        delta=abs(avg_price-float(price))  
        low_delta_sat=delta*100000000
        delta_percent=(delta/price)*100
        #print("----",low_delta_sat,avg_price,low_delta_percent)
        if delta_percent<float(threshold_percent):
            print("Should Send SMS LOW:",Coin.market)
        return delta_percent

    def check_24hr_high(Coin, threshold_percent=.5):
        avg_price=(float(Coin.bid))
        price=float(Coin.price_high_24hr)

        delta=abs(avg_price-float(price))
        low_delta_sat=delta*100000000
        delta_percent=(delta/price)*100
        #print("----",low_delta_sat,avg_price,low_delta_percent)
        if delta_percent<float(threshold_percent):
            print("Should Send SMS HIGH:", Coin.market)
        return delta_percent
    def add_coin_rules(self,coin,rule):
        self.to_do_list.append(coin,rule)
        