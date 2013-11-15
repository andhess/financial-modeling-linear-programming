import scipy as sp
from scipy import stats
import numpy as np
from read import *
import matplotlib.pyplot as plt

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

def showHistogram(data):
    hist, bins = np.histogram(data,bins = 50)
    print bins
    width = 0.7*(bins[1]-bins[0])
    center = (bins[:-1]+bins[1:])/2
    plt.bar(center, hist, align = 'center', width = width)
    plt.show()

def showDualLineGraph(data1, data2):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    time = np.arange(0, len(data2), 1)
    plt.plot(time, data2)

    plt.show()

def showLineGraph(data1):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    plt.show()

def showLineGraph(data, time):
    dataChunk = []
    for i in range(time-15, time+15):
        dataChunk.append(data[i])            
    time = np.arange(0, len(dataChunk), 1)
    plt.plot(time, dataChunk)
    plt.show()

def countNumIncreases(data):
    count = 0
    for i, part in enumerate(data):
        if i == 0:
            pass
        else:
            delta = data[i] - data[i-1]
            if delta > 0:
                count += 1
    print "Total timesteps =", len(data)-1, "\nTotal counted increases =", count, "\nResulting in P(increase) = ", str(float(count)/(len(data)-1))

def pUpGivenUpRun(data, runLength):
    upGivenRunCount = 0

    stepVizArray = []

    seenRunLength = False
    curRunCount = 0
    totRunCount = 0

    if runLength is 0:
        for i in range(len(data)):
            if i == 0:
                continue
            else:
                if data[i] - data[i-1] > 0:
                    upGivenRunCount += 1
        # print "Total # consecutive increase of runLength =", runLength, "\nTotal counted increases after seeing runLength consecutive increases =", upGivenRunCount, "\nResulting in P(increase | runLength consecutive increases ) = ", str(float(upGivenRunCount)/len(data))
        return float(upGivenRunCount)/len(data)
    else:
        for i, price in enumerate(data):
            if i == 0:
                continue
            else:
                diff = data[i] - data[i-1]
                if seenRunLength:
                    # seen runLength increases
                    totRunCount += 1
                    if diff > 0:
                        stepVizArray.append("+")
                        upGivenRunCount += 1
                    else:
                        stepVizArray.append("-")
                        seenRunLength = False
                        curRunCount = 0
                else:
                    if diff > 0:
                        stepVizArray.append("+")
                        curRunCount += 1
                        if curRunCount >= runLength:
                            seenRunLength = True
                    else:
                        stepVizArray.append("-")
                        curRunCount = 0

    # print "Total # consecutive increase of runLength =", runLength, "\nTotal counted increases after seeing runLength consecutive increases =", upGivenRunCount, "\nResulting in P(increase | runLength consecutive increases ) = ", str(float(upGivenRunCount)/totRunCount)
    # print stepVizArray
    if totRunCount is not 0:
        return float(upGivenRunCount)/totRunCount
    else:
        return 0.0

pep = []
# aapl = []
# f = []
# fb = []

readDataFromFile("./Historical-Datal/PEP.txt", pep)
# readDataFromFile("./Historical-Datal/aapl.txt", aapl)
# readDataFromFile("./Historical-Datal/F.txt", f)
# readDataFromFile("./Historical-Datal/fb.txt", fb)

pepOpenPrices = getOpenPriceHistory(pep)
# aaplOpenPrices = getOpenPriceHistory(aapl)
# fOpenPrices = getOpenPriceHistory(f)
# fbOpenPrices = getOpenPriceHistory(fb)
# print pepOpenPrices
# showHistogram(pepOpenPrices)



## Test for pUpGivenRun()
# testArray = [1,2,3,4,5,6,5,4,5,4,5,6,7,6,7,8,9,8,7,6,5,4,3,2,1,2,3,2,3,4,5,6,7,6,7]
# pUpGivenUpRun(aaplOpenPrices, 2)
# showLineGraph(pepOpenPrices)

# testresults = []
# for i in range(0,30):
#     testresults.append(("Run length "+ str(i), pUpGivenUpRun(testArray, i)))

# for res in testresults:
#     print res



def calculateSlope(data,t,numPoints):
    """
    Find the slope of the data at time t looking at the time t-numPoints to t
    t, t-1, t-2, .. t-numPoints+1

    return None for failures. 
    """
    print "Calculating slope at t =",t," and numPoints =",numPoints, " and length of data =", len(data)
    if data is None:
        print "None data passed"
        return None

    if t < 0:
        print "t must be greater than 0"
        return None
    if t >= len(data):
        print "t must be less than the length of data passed"
        return None

    if numPoints < 2:
        print "Must compare at least 2 points."
        return None
    if numPoints > t+1:
        print "t must be greater than num points"
        return None

    dataSlice = []
    # reverse iterate from data[t] down to data[t-numPoints] and put that in a list
    for i in range(t, t-numPoints, -1):
        if data[i] != None:
            dataSlice.append(data[i])
    dataSlice.reverse()

    print np.array(dataSlice)

    print np.gradient(dataSlice)
    print np.sum(np.gradient(dataSlice))/numPoints

    # showDualLineGraph(dataSlice, np.gradient(dataSlice))
    showLineGraph(dataSlice)
    showLineGraph(np.gradient(dataSlice))
    # showLineGraph(np.gradient(np.gradient(dataSlice)))

# testArray = [1,1,0,10]
# t = [100,81,64,49,36,25,16,9,4,1,0,1,4,9,16,25,36,49,64,81,100]

# calculateSlope(pepOpenPrices,1001,6)

# def findProbOfGainGivenSlope(data, patternSlope, patternLength):
    

showLineGraph(pepOpenPrices, 145)












