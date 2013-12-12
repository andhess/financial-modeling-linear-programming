import numpy as np
from AlphaBetaGammaFilter import AlphaBetaGammaFilter
import random
import math
from LinearFilter import LinearFilter
from wienerFilter import WienerPredictor

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
    def __init__(self, capital):
        self.assets = []
        self.availableCapital = capital

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

    def exitAll(self, lastPrice):
        for asset in self.assets:
            value = asset.unitsOwned * lastPrice

class TradingAlgorithm():
    """docstring for TradingAlgorithm"""
    def __init__(self, data, ticker, algorithm):
        self.data = data
        self.ticker = ticker
        self.capital = 100000
        self.portfolio = Porfolio(self.capital)
        self.algorithm = algorithm


    def run(self, parameter=None, method=None):
        actual = []
        predicted = []

        data = self.data
        ticker = self.ticker

        if parameter == None:
            parameter = 0.8

        # Kalman Filter / Alpha Beta Gamma Filter
        if self.algorithm == "abg":
            abgFilter = AlphaBetaGammaFilter(data[0],data[1],parameter)
            start = 0
        
        # Linear Model
        elif self.algorithm == "linearModel":
            filterLength = 2000
            stepLen = 1
            lf = LinearFilter(data[:len(data)/2],filterLength,stepLen)
            start = len(data)/2

        # Wiener Filter
        elif self.algorithm == "Wiener":
            steps = parameter
            format = method
            start = 4
            wF = WienerPredictor(data)

        # Double Moving Average
        elif self.algorithm == "dma":
            raise Exception("you need to use the DoubleMovingAverage Class for this algorithm!")

        else:
            raise Exception("No algorithm selected - Program Ending")


        # simulate over the range of the data
        currentPrice = 0
        projectedPrice = 0
        for t in range(start, len(data)-5):

            # if t % 1000 == 0:
            #     print t

            currentPrice = data[t]
            actual.append(currentPrice)

            if self.algorithm == "abg":
                projectedPrice = abgFilter.getProjectedValue(currentPrice)

            elif self.algorithm == "linearModel":
                projectedPrice = lf.applyFilter(t, data)

            elif self.algorithm == "Wiener":
                projectedPrice = wF.filter(t, steps, format)

            else:
                return

            predicted.append(projectedPrice)

            # print "\nIteration t =",t
            # print "Current price of", currentPrice, " projecting", projectedPrice

            if projectedPrice > currentPrice:
                # buy
                if self.portfolio.validateOrder(ticker, 1, currentPrice, "BUY"):
                    self.portfolio.placeOrder(ticker, 1, currentPrice, "BUY")
                else:
                    continue
            elif projectedPrice < currentPrice:
                # sell
                if self.portfolio.validateOrder(ticker, 1, currentPrice, "SELL"):
                    self.portfolio.placeOrder(ticker, 1, currentPrice, "SELL")
                else:
                    continue
            else:
                # hold
                continue

        # sell all assets
        for i in range(len(self.portfolio.assets)):
            self.portfolio.placeOrder(ticker, self.portfolio.assets[i].unitsOwned, currentPrice, "SELL")

        totalReturn = (self.portfolio.availableCapital - self.capital)
        return (totalReturn, actual, predicted)


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


class DoubleMovingAverage(TradingAlgorithm):
    """ Docstring for Double Moving Average"""

    def run(self, longW, shortW, noise=False):

        ticker = "PEP"

        # simulate over the range of the data
        currentPrice = 0
        self.addNoise = noise
        self.setNoise()
        self.longW = longW
        self.shortW = shortW

        prevDiff = 0

        for t in range( 6, len( self.data ) - 2 ):

            currentPrice = self.data[t]

            if t < self.longW:

                shortAvg = self.calcAverage(t, "short", int( t / (self.longW / self.shortW) ) )
                longAvg = self.calcAverage(t, "long", t)

            else:
                shortAvg = self.calcAverage(t, "short")
                longAvg = self.calcAverage(t, "long")
            
            currentDiff = longAvg - shortAvg

            # print "\nIteration t:  " , t

            if t == 0:
                continue

            # lines aren't crossing, do nothing
            if currentDiff > 0 and prevDiff > 0:
                continue

            # lines aren't crossing, do nothing
            elif currentDiff <= 0 and prevDiff <= 0:
                continue

            # sell!
            elif currentDiff > 0 and prevDiff <= 0:
                if self.portfolio.validateOrder(ticker, 1, currentPrice, "SELL"):
                    #print "Selling at", currentPrice
                    self.portfolio.placeOrder(ticker, 1, currentPrice, "SELL")
                    # self.printPortfolio()
                else:
                    pass
                    #print "order not valid. Tried selling at", currentPrice

            # buy!
            elif currentDiff <= 0 and prevDiff > 0:
                if self.portfolio.validateOrder(ticker, 1, currentPrice, "BUY"):
                    #print "Buying at", currentPrice
                    self.portfolio.placeOrder(ticker, 1, currentPrice, "BUY")
                    # self.printPortfolio()
                else:
                    pass
                    #print "order not valid. Tried buying at", currentPrice

            # shouldn't get here ever
            else:
                raise Exception("something wrong buy-sell cases")

            # update the previous values for the next state
            prevDiff = currentDiff

        # sell all assets

        # sell all assets
        if len( self.portfolio.assets ) > 0:
            self.portfolio.placeOrder(ticker, self.portfolio.assets[0].unitsOwned, currentPrice, "SELL")

        totalReturn = (self.portfolio.availableCapital - self.capital)
        return totalReturn


    def calcAverage(self, time, windowType, windowLength=None):

        if windowType == "long":
            window = self.longW if windowLength is None else windowLength
            avg = np.array( self.data[time-window:time+1] )

        else:
            window = self.shortW if windowLength is None else windowLength
            avg = np.array( self.data[time-window:time+1] )

        if self.addNoise:
            if windowType == "long":
                return np.average( avg + np.array( self.noise[time-window:time+1] ) )
            else:
                return np.average( avg + np.array( self.noise[time-window:time+1] ) )
        else:
            return np.average( avg )


    def setNoise(self):
        noise = []
        if self.addNoise:
            for i in range(len(self.data)):
                noise.append( random.gauss(0, self.sigma) )
        else:
            for i in range( len( self.data ) ):
                noise.append( 0 )

        self.noise = noise

