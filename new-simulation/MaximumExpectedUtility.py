import random
import numpy as np

def weighted_choice(weights):
    """ Random weighted selection
    Given [2,3,5] this function returns 
    0 with .2 prob
    1 with .3 prob
    2 with .5 prob
    """
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i

class MEU():
    """MEU"""
    def __init__(self, data):
        self.data = data

        # utilities are the following form: Decision and Event
        # [buy and up, buy and down, sell and up, sell and down]
        self.utilities = [100, 0, 25, 100]
        self.accuracy = 0.7

    def getDecision(self, time):
        currentPrice = self.data[time]
        realNextPrice = self.data[time+1]

        # decide whether to introduce noise
        estimatedNextPrice = None
        choice = weighted_choice([self.accuracy,1.0-self.accuracy])
        if choice == 0: # don't add noise
            estimatedNextPrice = realNextPrice
        else: # add 3-sigma range white gaussian noise
            avgPriceChange = np.average(self.data)
            stdDevPriceChange = np.std(self.data)
            noiseRange = avgPriceChange + 2*stdDevPriceChange
            coinFlip = random.randint(1,100)
            if coinFlip > 50:
                estimatedNextPrice = currentPrice + random.random()*noiseRange
            else:
                estimatedNextPrice = currentPrice - random.random()*noiseRange
            

        estimatedPriceChange = estimatedNextPrice - currentPrice


        pUp = None
        if estimatedNextPrice > currentPrice:
            pUp = self.accuracy
        else:
            pUp = 1.0 - self.accuracy

        # Expected Utility (BUY)
        buyAndUp = self.utilities[0]
        buyAndDown = self.utilities[1]
        expectedUtilityBuy = buyAndUp*pUp + buyAndDown*(1.0-pUp)

        # ExpectedUtility (SELL)
        sellAndUp = self.utilities[2]
        sellAndDown = self.utilities[3]
        expectedUtilitySell = sellAndUp*pUp + sellAndDown*(1.0-pUp)


        if expectedUtilityBuy > expectedUtilitySell:
            return "BUY"
        else:
            return "SELL"


# meu = MEU([10,8,6,9,11,13])

# bCount = 0
# sCount = 0
# for i in range(10000):
#     d = meu.getDecision(3)
#     if d == "BUY":
#         bCount += 1
#     else:
#         sCount += 1

# print "Decided to buy", bCount,"times and sell",sCount, "times. total=",bCount+sCount




