import unittest

from crypto import Coin, Exchange,Rule

class TestCoin(unittest.TestCase):
    def test_init(self):
        e=Exchange(None,None,Exchange.EX_BINANCE)
        c=Coin('TRX','BTC',e)


        #self.assertEqual('s',1)
if __name__ == '__main__':
    unittest.main()