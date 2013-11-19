import common
import portolioItem
import investmentStrategy

def simulateTradingStrategy( data, startTime, desiredReturn, riskTolerance, weights ):
    """

    """

    global time
    global portfolio
    global positionHistory
    global availableCapital
    
    # --- Initialization ---

    # create investmentStrategy to remember the important stuff
    positionHistory = investmentStrategy.InvestmentStrategy( availalableCapital )

    # create portfolio objects
    for i, dataSet in enumerate( data ):
        symbol = data[i][0]
        del data[i][0]
        portflio.append( PortfolioItem( symbol, data, weights ) )
        positionHistory.addInstrument( symbol )

    totalTime = len( data[0] )
    tradingTime = totalTime - startTime - 1

    # --- Pre-Processing ---

    # train the weights

    while time <= startTime:
        for j, instrument in enumerate( portfolio ):
            instrument.description.train( time )

        time += 1

    # --- Trading Period ---

    while time < totalTime:

        # get description

        # make decision

        time += 1

        # training