import description

class PortfolioItem:


    def __init__(self, symbol, data, features):

        self.symbol         =   symbol
        self.previousValue  =   0
        self.currentValue   =   0
        self.z              =   0
        self.numPositions   =   0
        self.description    =   DescriptionModel( data, features )

    def updateEquityPrice(self, newPrice):
        self.previousValue = self.currentValue
        self.currentValue = newPrice