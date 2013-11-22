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

def  simulateTradingStrategy(previousData, futureData, stepSize, desiredReturn, riskTolerance, listOfWeights):
    """
    previousData        :   A set of equities and their previous data
    futureData          :   A set of the same equities but their performance over the next tradingPeriod
    stepSize            :   The time interval on which each equity price is given
    desiredReturn       :   Desired return, a percentage of initial capital
    riskTolerance       :   Tolerance to risk. Current risk value is not to exceed this at any time
    listOfWeights       :   These are the features that we want to study trends in

    the first index of previousData and futureData will contain the symbol of the stock
    this program anticipates each index of the past/future data being in the same order
    s.t. previousData[i] is for the same symbol as futureData[i]
    it is also assumed that all data has the same level of resolution. Any inconsistencies will not work
    """

    global equities
    global availableCapital
    equityNames = []

    numIntervalsToTrade = len(futureData[0])
    trainIntervals = numIntervalsToTrade - 1

    # create equity object for set in previousData
    for i, data in enumerate(previousData):
        equities.append( equity.Equity( data[i][0], data[i][1][1], 0, listOfWeights ))
        equityNames.append(data[i][0])

        # now remove symbol from list of data
        del previousData[i][0]
        del futureData[i][0]

    # train the weights
    for j, equity in enumerate(equities):
        equity.weights.prevTraining( previousData[j] ):

    # also need to do one more train for 1st of futureData
    for l, equity in enumerate(equities):
        equity.weights.singleTrain( previousData[l], futureData[l][0] )

    # create investmentStrategy object
    positionHistory = investmentStrategy.InvestmentStrategy(availableCapital, equityNames)

    # now let the investment begin
    for i in range(0, numIntervalsToTrade):

        # make prediction of next step
        for j, equity in enumerate(equities):
            equity.predictedValue = equity.weights.predict( previousData[j], futureData[j][i] )

        # make moves for next step
        investCapital()

        # will there be another step?
        if i != trainIntervals:

            # teach each equity from current data
            for k, equity in enumerate(equities):

                # current data is now old data
                previousData[k].append( futureData[k][i] )

                # train from this tick
                equity.weights.singleTrain( previousData[k], futureData[k][i + 1] )


def investCapital():
    global equities

    # optimization shit needs to go here

    investmentStrategy.recordPositions(equities)
    pass