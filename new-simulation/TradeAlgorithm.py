import numpy as np
from AlphaBetaGammaFilter import AlphaBetaGammaFilter
import random
from LinearFilter import LinearFilter

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
            if self.availableCapital > order.getTotalValue():
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
        return True


class TradingAlgorithm():
    """docstring for TradingAlgorithm"""
    def __init__(self, dataList, tickerList):
        self.dataList = dataList
        self.tickerList = tickerList
        self.capital = 100000
        self.portfolio = Porfolio()


    def run(self):
        buys = []
        sells = []
        tradeRates = []
        totReturns = []
        actualPrices = []
        predictedPrices = []

        for i in range(len(self.tickerList)):
            oldAvailableCapital = self.portfolio.availableCapital
            actual = []
            predicted = []

            data = self.dataList[i]
            ticker = self.tickerList[i]

            abgFilter = AlphaBetaGammaFilter(data[0],data[1],0.65)

            filterLength = 2000
            stepLen = 1
            # lf = LinearFilter(data,filterLength,stepLen)

            # simulate over the range of the data
            currentPrice = 0
            projectedPrice = 0
            buyCount = 0
            sellCount = 0
            for t in range(len(data)-2):
                currentPrice = data[t]
                actual.append(currentPrice)
                projectedPrice = abgFilter.getProjectedValue(currentPrice)
                # projectedPrice = lf.applyFilter(t)
                predicted.append(projectedPrice)


                # print "\nIteration t =",t
                # print "Current price of", currentPrice, " projecting", projectedPrice

                if projectedPrice > currentPrice and projectedPrice - currentPrice > .05:
                    # buy
                    if self.portfolio.validateOrder(ticker, 1, currentPrice, "BUY"):
                        # print "Buying at", currentPrice, " projecting", projectedPrice
                        self.portfolio.placeOrder(ticker, 1, currentPrice, "BUY")
                        # self.printPortfolio()
                        buyCount += 1
                    else:
                        print "order not valid. Tried buying at", currentPrice, " projecting", projectedPrice
                elif projectedPrice < currentPrice and currentPrice - projectedPrice > .05:
                    # sell
                    if self.portfolio.validateOrder(ticker, 1, currentPrice, "SELL"):
                        # print "Selling at", currentPrice, " projecting", projectedPrice
                        self.portfolio.placeOrder(ticker, 1, currentPrice, "SELL")
                        # self.printPortfolio()
                        sellCount += 1
                    else:
                        continue
                        # print "order not valid. Tried selling at", currentPrice, " projecting", projectedPrice
                else:
                    # hold
                    continue
                    # print "hold"
            # print "Buys:", buyCount, "Sells:", sellCount
            buys.append(buyCount)
            sells.append(sellCount)
            tradeRates.append((buyCount+sellCount) / 251.0)
            totReturns.append(oldAvailableCapital-self.portfolio.availableCapital)
            actualPrices.append(actual)
            predictedPrices.append(predicted)

            # self.printPortfolio(currentPrice)

        # print self.tickerList
        # print buys
        # print sells
        # print tradeRates
        # print totReturns
        # print actualPrices[0][400:500]
        # print predictedPrices[0][400:500]
        print [i for i in range(100)]


    def printPortfolio(self, currentPrice):
        print "Current portfolio status:"
        print "Number assets =", len(self.portfolio.assets), " with availableCapital =",self.portfolio.availableCapital
        tot = 0
        for a in self.portfolio.assets:
            print "\t",a.unitsOwned, " units of", a.ticker, "owned."
            tot += a.unitsOwned * currentPrice
        #     for o in a.orderHistory:
        #         print "\t\t", o.orderType, "", o.count, "at", o.purchasePrice
        print "Total Value =", self.portfolio.availableCapital + tot


