import common
import portolioItem
import investmentStrategy

def simulateTradingStrategy( data, startTime, desiredReturn, riskTolerance, weights ):
    """

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

        common.time += 1

        # training