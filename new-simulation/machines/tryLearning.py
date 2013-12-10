import math

weights = [0.25, 0.25, 0.25, 0.25]
tolerance = 0.02

# treat decisionMakers like the threshold for a particular decision
# sell < 0, hold < 0.3, buy > 0.3
decisionMakers = [0, 0.25]

# read
data = get-the-data!

# for testing, remove the symbol
del data[0]




def mainTraining():

    global data
    global weights
    global tolerance
    global decisionMakers

    time = 0
    totalTime = len(data)

    for i range(totalTime - 1):

        # get properties
        stats = properties()

        prediction = prediction(stats)

        # compare the prediction with real result

#       HOW COMPARE?
#           - prediction gives a Z value
#           - Z value tells model which decision to make
#           - want to quantatively access the decision that it made
#           - get return between next tick
#           - based on given decision, assess the following:
#               - was the situation the right choice?
#               - should Z have been higher or lower?
        
        currentTickOpen = data[i][1]
        nextTickOpen = data[i+1][1]

        # what did the decision model tell us to do?
        actualDecision = decisionModel(prediction) # FIXME

        # a couple different ways to compare
        logDif = math.log(nextTickOpen / currentTickOpen)
        percentDif = (nextTickOpen - currentTickOpen) / currentTickOpen

        # what should the decision have been?
        expectedDecisionLog = ''
        expectedDecisionCent = ''
        
        # ---- natural log ----

        # buy or sell
        if math.fabs(logDif) - tolerance > 0:
            if logDif < 0:
                expectedDecisionLog = 'sell'
            else:
                expectedDecisionLog = 'buy'
        # hold
        else:
            expectedDecisionLog = 'hold'

        # was the right decision made? (actual-expected)
        # ---- log ----
        if expectedDecisionLog == actualDecision:

            # case buy-buy

            # case hold-hold

            # case sell-sell

        else:

            # Z too low
            # sell-buy
            # sell-hold
            # hold-buy

            # Z too high
            # buy-sell
            # buy-hold
            # hold-sell


        # ---- percent ----
        # buy or sell
        if math.fabs(percentDif) - tolerance > 0:
            if percentDif < 0:
                expectedDecisionCent = 'sell'
            else:
                expectedDecisionCent = 'buy'
        # hold
        else:
            expectedDecisionCent = 'hold'

def predict(stats):
    global weights
    zVal = 0
    for i in range( len(stats) ):
        zVal += weights[i] * stats[i]

    return zVal


mainTraining()