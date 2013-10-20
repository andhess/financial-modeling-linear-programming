class Equity:
    """
    An equity keeps track of a speciic stock index
    It has a symbol, currentValue, previousValue
    It also keeps track of the number of positions one currently holds in a portfolio
    """

    def __init__(self, symbol, currentValue, previousValue):
        self.symbol = symbol
        self.currentValue = currentValue
        self.previousValue = previousValue
        self.numPositions = 0

    def updateEquityPrice(self, newPrice):
        """
        update the price of an equity
        """
        self.previousValue = self.currentValue
        self.currentValue = newPrice

    def purchaseEquity(self, amountToInvest, totalCapital):
        """
        input: amount of capital wishing to invest, total liquid capital
        attempts to purchase as much as possible
        output: total remaining liquid capital after purchase
                i.e. the new availableCapital
        """

        if totalCapital < amountToInvest:
            throw Exception()

        # can only buy integer values
        self.numPositions = math.floor( amountToInvest / self.currentValue )
        return totalCapital - self.numPositions * self.currentValue

    def sellEquity(self, numSharesToSell):
        """
        input: number of shares wishing to sell
        output: capital earned by selling shares
        """
        if numSharesToSell < self.numPositions:
            print "Do not own enough shares"
            raise Exception()
        value = numSharesToSell * self.currentValue
        self.numPositions = numSharesToSell - self.numPositions
        return value

    def exitPosition(self):
        """
        sell off all shares of equity
        """
        value = self.numPositions * self.currentValue
        self.numPositions = 0
        return value