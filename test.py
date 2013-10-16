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
    for i, price in enumerate(data):
        if i == 0:
            pass
        else:
            delta = data[i] - data[i-1]
            if seenRunLength:
                # seen runLength increases
                totRunCount += 1
                if delta > 0:
                    stepVizArray.append("+")
                    upGivenRunCount += 1
                else:
                    stepVizArray.append("-")
                    seenRunLength = False
                    curRunCount = 0
            else:
                if delta > 0:
                    stepVizArray.append("+")
                    curRunCount += 1
                    if curRunCount >= runLength:
                        seenRunLength = True
                else:
                    stepVizArray.append("-")
                    curRunCount = 0

    print "Total # consecutive increase of runLength =", totRunCount, "\nTotal counted increases after seeing runLength consecutive increases =", upGivenRunCount, "\nResulting in P(increase | runLength consecutive increases ) = ", str(float(upGivenRunCount)/totRunCount)
    # print stepVizArray


pep = []
aapl = []
f = []
fb = []

readDataFromFile("./Historical-Datal/PEP.txt", pep)
readDataFromFile("./Historical-Datal/aapl.txt", aapl)
readDataFromFile("./Historical-Datal/F.txt", f)
readDataFromFile("./Historical-Datal/fb.txt", fb)


pepOpenPrices = getOpenPriceHistory(pep)
aaplOpenPrices = getOpenPriceHistory(aapl)
fOpenPrices = getOpenPriceHistory(f)
fbOpenPrices = getOpenPriceHistory(fb)


# print openPrices
# showHistogram(openPrices)

testArray = [1,1,1,1,2,3,3,4,5,6,7]
pUpGivenUpRun(aaplOpenPrices, 2)
showLineGraph(aaplOpenPrices)

