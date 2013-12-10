import common
import numpy as np
import description
from TradeAlgorithm import *
import matplotlib.pyplot as plt


def showHistogram(data):
    hist, bins = np.histogram(data,bins = 20)
    print bins
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center', width = width)
    plt.show()

def showLineGraph(data1):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    plt.show()

def showDualLineGraph(data1, data2):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    time = np.arange(0, len(data2), 1)
    plt.plot(time, data2)

    plt.show()


dataList = []
#tickerList = ["PEP", "aapl", "ACN", "CAT", "F", "M", "UPS", "PCLN", "CPB"]
tickerList = ["F"]

for ticker in tickerList:
    rawReadData = []
    dataPath = "./../Historical-Datal/" + ticker + ".txt"
    description.readDataFromFile(dataPath, rawReadData)
    data = description.getOpenPriceHistory(rawReadData)
    dataList.append(data)

ta = TradingAlgorithm(dataList, tickerList)
ta.run()





def simulateTradingStrategy( data, startTime, desiredReturn, riskTolerance, weights ):
    """
    simulates trading over a set of data with given attributes to look for and desired performance

    Inputs:
    [array] data            :   contains ticker data for a set of financial instruments
    (int)   startTime       :   the time at which trading will begin
    (float) desiredReturn   :   the desired return on investment (0.25 == 25%)
    (float) riskTolerance   :   the 
    [array] weights         :   the features upon which decisions are to be made

    Outputs:
    (float)     actualRisk      :   the actual risk associated with the portfolio
    (float)     actualReturn    :   the actual return on investment
    (Object) InvestmentStrategy :   an object detailing all positions ever held

    Explanation of data:

    data = [ [instrument-0], [instrument-1], [instrument-2], ... , [instrument-n] ]
    
    [array] instrument-i = [ tickerSymbol, [tick-0],[tick-1], ... , [tick-n] ]
    
    (String) tickerSymbol   :   the symbol that refers to the given financial instrument
                ex. "FB" = Facebook, "TSLA" = Tesla Motors    
    
    [array] tick-j = [ timeComponents, openPrice, highPrice, lowPrice, closePrice ]

    (datetime)  timeComponents  :   a datetime object for the start of the given period
    (float)     openPrice       :   the price at which the instrument opened at for the period
    (float)     highPrice       :   the value at which the instrument was highest for the period
    (float)     lowPrice        :   the value at which the instrument was lowest for the period
    (float)     closePrice      :   the price at which the instrument closed at for the period

    weights = [ feature-1, feature-2, ... , feature-n ]
        (string) feature-k  :   name of the feature considered in the model 

    """

    global time
    global portfolio
    
    # --- Initialization ---

    # create investmentStrategy to remember the important stuff
    common.positionHistory = investmentStrategy.InvestmentStrategy( common.availalableCapital )

    # create portfolio objects
    for i, dataSet in enumerate( data ):
        symbol = data[i][0]
        del data[i][0]
        common.portfolio.append( portfolioItem.PortfolioItem( symbol, data, weights ) )
        common.positionHistory.addInstrument( symbol )

    totalTime = len( data[0] )
    tradingTime = totalTime - startTime - 1

    # --- Pre-Processing ---

    # train the weights

    while common.time <= startTime:
        for j, instrument in enumerate( common.portfolio ):
            instrument.description.train( common.time )

        common.time += 1

    # --- Trading Period ---

    while common.time < totalTime:

        # get description

        # make decision

        # record positions
        for instrument in common.portfolio:
            common.positionHistory.recordPosition( instrument.symbol, instrument.currentValue, instrument.numPositions )

        common.positionHistory.calculateValue()

        common.time += 1

        # training