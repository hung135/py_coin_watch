class SymbolStruct():
    def __init__(self, symbol,hodl=0,basemarket='BTC',misc=None,all_exchange=False,name=None):
        self.symbol = symbol
        self.basemarket = basemarket
        self.hodl = hodl
        self.misc = misc
        self.all_exchange=all_exchange
        self.name=name