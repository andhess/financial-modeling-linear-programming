import math
import datetime
# import KalmanFilter
# import LinearFilter
from AlphaBetaGammaFilter import AlphaBetaGammaFilter
import scipy.stats
import numpy as np
# import matplotlib.pyplot as plt

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



class DescriptionModel( object ):
    
    global learning

    """  """
    def __init__( self, data, features ):
        self.data = data

        n = len( features )
        val = 1.0 / n
        self.weights = {}

        for item in features:
            self.weights[item] = val

    def getObjectiveFunctionValue(self, time):
        """
        gets the value for existing weight values and the features currently
        observed in the model

        Input:
        time    :   the current time in the whole model
        """

        z = 0.0
        for feature in self.weights:
            z += self.weights[feature] * self.getCurrentFeature(feature, time) 

        return z

    def getCurrentFeature( self, feature, time ):
        """
        determine which feature function to run

        Inputs:
        time    :   the current time in the model
        feature :   the feature desired to be selected
        """

        # expand this list as more features are added
        if feature == "acceleration":
            return self.getAcceleration( time )
        elif feature == "velocity":
            return self.getVelocity( time )
        elif feature == "kalman":
            return self.getKalmanFilter( time )
        elif feature == "linear":
            return self.getLinearFilter( time )
        else:
            return 0

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

    def getFilterProjection(self, time):
        correlationList = []
        # filterLength = 2500
        for filterLength in range(500,4501,500):
            stepLen = 1
            lf = LinearFilter(self.data,filterLength,stepLen)
            expectedGains, actualGains = [], []
            for i in range(filterLength+1,len(self.data)-100):
            # for i in range(1001,1020):
                projectedValue = lf.applyFilter(i)
                expectedGain = float(projectedValue) - self.data[i]
                
                actualGain = self.data[i+1] - self.data[i]

                expectedGains.append(expectedGain)
                actualGains.append(actualGain)

            correlation = (stepLen, scipy.stats.pearsonr(expectedGains, actualGains))
            correlationList.append(correlation)
            # showDualLineGraph(expectedGains, actualGains)
            # showLineGraph(np.array(expectedGains)-np.array(actualGains))
            print correlation

        showLineGraph(np.array(correlationList))
        return (expectedGain, actualGain)

    # def training( self, time ):



def showDualLineGraph(data1, data2):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    time = np.arange(0, len(data2), 1)
    plt.plot(time, data2)

    plt.show()

# rawReadData = []
# ticker = "PEP"
# dataPath = "./../Historical-Datal/" + ticker + ".txt"
# readDataFromFile(dataPath, rawReadData)
# data = getOpenPriceHistory(rawReadData)

# for e in data:
#     print e

# abg = AlphaBetaGammaFilter(data)
# (actual, projected) = abg.getProjectedValue(.65)

# for i in range(100):
#     print str(actual[i]) + "\t" + str(projected[i])

# correlationList = []

# for i in range(10,100,10):
#     alpha = float(i)/100.0

#     filtr = AlphaBetaGammaFilter(data)
#     actualValues, projectedValues = filtr.getProjectedValue(alpha)

#     showDualLineGraph(actualValues[1000:1050], projectedValues[1000:1050])
    # correlation = (alpha, scipy.stats.pearsonr(projectedValues, data))
    # correlationList.append(correlation)


# print correlationList




