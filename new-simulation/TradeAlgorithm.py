import numpy as np
from AlphaBetaGammaFilter import AlphaBetaGammaFilter

class Order():
    """ A datatype for an order object 
    ticker          : stock ticker 'TSLA'
    count           : total number of units purchased
    purchasePrice   : price of equity at the time of the order
    orderType       : 'BUY' or 'SELL'

    """

    def __init__(self, ticker, count, purchasePrice, orderType):
        self.ticker = ticker
        self.count = int(count)
        self.purchasePrice = float(purchasePrice)
        self.orderType = orderType

    def getTotalValue(self):
        """ Return the total value of the order. """
        return self.count * self.purchasePrice

class Asset():
    """ A class to model an asset as part of the Portfolio
    ticker          : stock ticker 'TSLA'
    unitsOwned      : the total number of units owned
    orderHistory    : an archive of all of the orders placed on this asset

    """
    def __init__(self, ticker):
        self.ticker = ticker
        self.unitsOwned = 0
        self.orderHistory = []

    def addOrder(self,order):
        """ Record the order and modify the units owned appropriately 
        Parameters:
            order   : an Order class for a given security. 
        """
        self.orderHistory.append(order)
        if order.orderType == "BUY":
            self.unitsOwned += order.count
        else:
            self.unitsOwned -= order.count
        
        
class Porfolio():
    """ A datatype for a trading portfolio. 
    
    assets              : a list of assets in the portfolio
    availableCapital    : total amount of capital available to invest
    """
    def __init__(self):
        self.assets = []
        self.availableCapital = 100000

    def placeOrder(self, ticker, count, price, orderType):
        """ Handle both buy and sell orders """
        # create the order to place
        order = Order(ticker, count, price, orderType)

        # handle a buy order
        if orderType == "BUY":
            # check to see if we have the available capital
            if availableCapital > order.getTotalValue():
                # subtract the order value from the capital pool
                self.availableCapital -= order.getTotalValue()
                
                # if we have purchased this equity before, add to the order history
                inPortfolio = False
                for a in self.assets:
                    if a.ticker == order.ticker:
                        inPortfolio = True
                        a.addOrder(order)
                
                # have not purchased before, add new asset object
                if not inPortfolio:
                    newAsset = Asset(order.ticker)
                    newAsset.addOrder(order)
                    self.assets.append(newAsset)

                # successfuly placed order
                return True
            else:
                # failed to place order
                return False
        # handle a sell order
        else: 
            inPortfolio = False
            for a in self.assets:
                if a.ticker == order.ticker:
                    # make sure we have enough units to sell
                    if a.unitsOwned >= order.count:
                        inPortfolio = True
                        a.addOrder(order)
                         # subtract the order value from the capital pool
                        self.availableCapital += order.getTotalValue()
                    else:
                        # not enough units owned, order failed
                        return False

            if not inPortfolio:
                return False

    def validateOrder(self, ticker, count, price, orderType):
        """ Each order that is placed has to be validated. """
        
        # buy side validatin
        if orderType == "BUY":
            # make sure there is enough available capital
            orderValue = count*price
            if orderValue >= self.availableCapital:
                return False
        # sell side validation
        else:
            # ensure we have the asset to sell
            inPortfolio = False
            for a in self.assets:
                if a.ticker == ticker:
                    inPortfolio = True
                    if a.unitsOwned < count:
                        return False
            if not inPortfolio:
                return False


class TradingAlgorithm():
    """docstring for TradingAlgorithm"""
    def __init__(self, data):
        self.data = data
        self.capital = 100000
        self.portfolio = Porfolio()


    def run(self):
        # abgFilter = AlphaBetaGammaFilter(data)

        ticker = "PEP"
        # simulate over the range of the data
        for t in range(data):
            currentPrice = data[t]
            projectedPrice = abgFilter.getProjectedValue(t)
            
            if projectedPrice > currentPrice:
                # buy
                if self.portfolio.validateOrder(ticker, 1, currentPrice, "BUY")
                    self.portfolio.placeOrder(ticker, 1, currentPrice, "BUY")
                else:
                    print "order not valid"
            elif projectedPrice < currentPrice:
                # sell
                if self.portfolio.validateOrder(ticker, 1, currentPrice, "SELL")
                    self.portfolio.placeOrder(ticker, 1, currentPrice, "SELL")
                else:
                    print "order not valid"
            else:
                # hold
                print "hold"







