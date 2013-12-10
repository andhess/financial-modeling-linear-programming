import common
# import portolioItem
# import investmentStrategy
import description
from TradeAlgorithm import *


rawReadData = []
ticker = "AAPL"
dataPath = "./../Historical-Datal/" + ticker + ".txt"
description.readDataFromFile(dataPath, rawReadData)
data = description.getOpenPriceHistory(rawReadData)

ta = TradingAlgorithm(data)
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