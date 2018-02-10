
class Rule:
    to_do_list=None
    
    def check_24hr_low(coin,threshold_percent=.5):
        avg_price=(float(coin.sell))
        price=float(coin.price_low_24hr)

        delta=abs(avg_price-float(price))  
        low_delta_sat=delta*100000000
        delta_percent=(delta/price)*100
        #print("----",low_delta_sat,avg_price,low_delta_percent)
        if delta_percent<float(threshold_percent):
            print("Should be Sending SMS")
        return delta_percent

    def check_24hr_high(coin,threshold_percent=.5):
        avg_price=(float(coin.bid))
        price=float(coin.price_high_24hr)

        delta=abs(avg_price-float(price))
        low_delta_sat=delta*100000000
        delta_percent=(delta/price)*100
        #print("----",low_delta_sat,avg_price,low_delta_percent)
        if delta_percent<float(threshold_percent):
            print("Shouldn be Sending SMS")
        return delta_percent
    def add_coin_rules(self,coin,rule):
        self.to_do_list.append(coin,rule)
        