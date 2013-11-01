import equity
import common
import investmentStrategy


def calculateStepSize(stockData):
    """
    stockData is the same as previousData or futureData
    returns a timedelta object
    """
    t1 = stockData[0][1][0]
    t2 = stockData[0][2][0]
    stepSize = t2 - t1

    return stepSize

def  simulateTradingStrategy(previousData, futureData, stepSize, desiredReturn, riskTolerance):
    """
    previousData        :   A set of equities and their previous data
    futureData          :   A set of the same equities but their performance over the next tradingPeriod
    stepSize            :   The time interval on which each equity price is given
    desiredReturn       :   Desired return, a percentage of initial capital
    riskTolerance       :   Tolerance to risk. Current risk value is not to exceed this at any time

    the first index of previousData and futureData will contain the symbol of the stock
    this program anticipates each index of the past/future data being in the same order
    s.t. previousData[i] is for the same symbol as futureData[i]
    it is also assumed that all data has the same level of resolution. Any inconsistencies will not work

    """

    global equities
    global availableCapital
    equityNames = []

    numIntervalsToTrade = len(futureData)

    # create equity object for everything in trading period
    for i, data in enumerate(futureData):
        equities.append(equity.Equity( data[i][0], data[i][1][1], previousData[i][futureData - 1][1] ))
        equityNames.append(data[i][0])

        # now remove symbol from list of data
        del previousData[i][0]
        del futureData[i][0]

    # create investmentStrategy object
    positionHistory = investmentStrategy.InvestmentStrategy(availableCapital, equityNames)

    # now let the investment begin
    for i, tick in enumerate(futureData):

        investCapital()

        # prepare for next step
        previousData.append(tick)

def investCapital():
    global equities

    # optimization shit needs to go here

    investmentStrategy.recordPositions(equities)
    pass