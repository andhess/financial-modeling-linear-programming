import numpy as np
import scipy.stats
import datetime

import scipy as sp
from scipy import stats
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

def readDataFromFile(fileName, outputList):
    # open the file from bloomberg

    fl = open(fileName, "r")

    # ignore the first line
    #fl.readline()

    for i, line in enumerate(fl):

        entry = []

        if line.startswith("Symbol"):
            name = line.replace("\t", " ").replace("\r\n", "").split(" ")
            outputList.append(name[1])
            continue

        elif line.startswith("Date"):
            continue

        elif line.startswith("\r\n"):
            continue

        line = line.replace("\t", " ").replace("\r\n", "")

        snapshot = line.split(" ")

        # get date and time of snapshot
        dateComponents = snapshot[0].split("-")
        year = int(dateComponents[0])
        month = int(dateComponents[1])
        day = int(dateComponents[2])

        timeComponents = snapshot[1].split(":")
        hour = int(timeComponents[0])
        minute = int(timeComponents[1])
        second = int(timeComponents[2])

        timestamp = datetime.datetime(year, month, day, hour, minute, second)

        # Get financial data
        openPrice = float(snapshot[2])
        highPrice = float(snapshot[3])
        lowPrice = float(snapshot[4])
        closePrice = float(snapshot[5])

        entry.append((timestamp, openPrice, highPrice, lowPrice, closePrice))

#        if len(snapshot) > 6:
#            tradeVolume = int(snapshot[6])
#            entry.append(tradeVolume)

        # Store tuple of snapshot data in list
        outputList.append(entry)

    fl.close()


def getOpenPriceHistory(data):
    """
    Given an array of tuples in the form: (Date, Open, High, Low, Close, Volume)
    return a list of the openPrices.  
    """
    priceHistory = list()
    
    for snapshot in data:
        openPrice = snapshot[0][1]
        priceHistory.append(openPrice)
    return priceHistory



class DescriptionModel(object):
    
    """  """
    def __init__(self, data):
        self.data = data

        # normalize
        # total = float(self.totalCount())
        # if total == 0: return
        # for key in self.keys():
        #     self[key] = self[key] / total

        self.featureFunctions = [self.getVelocity, self.getAcceleration]
        self.weights = [1,1]

        # normalize the weights to initialize
        self.normalizeWeights()
        

    def getObjectiveFunctionValue(self, time):
        z = 0.0
        for i in xrange(len(self.weights)):
            z += self.weights[i] * self.featureFunctions[i](time)
        return z

    def normalizeWeights(self):
        total = float(len(self.weights))
        if total == 0: return
        for i, w in enumerate(self.weights):
            self.weights[i] = w / total

    def getActualReturn(self, time, endTime=0):
        """ Get the actual return of the equity by returning the difference of 
        the final price and the price at the time passed. 

        data: a list of price history
        time: the specified time 
        endTime: end time optional parameter

        examples
            data = [1,2,3,4]
            getExpectedReturn(1, 3)
            => 4-2 = 2

        """
        if endTime != 0 and time < len(self.data):
            # use the final value
            return self.data[-1] - self.data[time]
        elif endTime > time:
            # use the specified end time 
            return self.data[endTime-1] - self.data[time-1]
        else:
            # return none in case of malformed input
            return None


    def getVariance(self):
        """
        Calculate and return the variance of the data. 
        """
        return scipy.stats.variation(self.data)

    def getVelocity(self, time, span=10):
        """ Return the average velocity of the data up to time t going back 'span' units in time
            Velocity = (change in y)/(change in x)

            span: the number of points to capture the velocity for. 
            time: the time we are looking to get a slope for

        """
        # Calculate the slope using rise/run
        # print self.data
        # print self.data[time]
        # print self.data[time-span+1]
        # print span-1
        # print "results in: ", (self.data[time] - self.data[time - span + 1]) / float(span-1)


        dataSlice = []

        # get a chunk of dat with size specified by "span"
        for i in range(time - span + 1, time +1):
            if self.data[i] != None:
                dataSlice.append(self.data[i])

        # return the average of the velocities in the span
        return np.sum(np.gradient(dataSlice))/float(span)

    def getAcceleration(self, time, span=10):
        dataSlice = []

        # get a chunk of the data to calculate over
        for i in range(time - span + 1, time + 1):
            if self.data[i] != None:
                dataSlice.append(self.data[i])

        # the average acceleration
        return np.sum(np.gradient(np.gradient(dataSlice)))/float(span)


class DecisionModel():
    """docstring for DecisionModel"""
    def __init__(self, descriptionModel):
        self.descriptionModel = descriptionModel

    def getPossibleActions(self):
        return ["buy", "hold", "sell"]

    def getPolicyDecision(self, time):
        # get the z value from the objective function
        z = self.descriptionModel.getObjectiveFunctionValue(time)

        if z > .001:
            return "buy"
        else if z < -.001:
            return "sell"
        else:
            return "hold"


class WeightEstimationModel():
    """docstring for WeightEstimationModel
    A model for estimating the optimal weights of features in our
    objective function. 
    """

    def __init__(self, ticker):
        rawReadData = []
        dataPath = "./../Historical-Datal/" + ticker + ".txt"
        readDataFromFile(dataPath, rawReadData)
        data = getOpenPriceHistory(rawReadData)

        # create a description model for the equity
        self.descriptionModel = DescriptionModel(data)



wem = WeightEstimationModel("PEP")

objFuncValues = []
for t in xrange(len(wem.descriptionModel.data)):
    objFuncValues.append(wem.descriptionModel.getObjectiveFunctionValue(t))

showLineGraph(objFuncValues)
# print wem.descriptionModel.getObjectiveFunctionValue(148)
# print wem.descriptionModel.data



















        

