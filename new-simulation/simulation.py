import common
import numpy as np
import description
from TradeAlgorithm import *
# import matplotlib.pyplot as plt


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

def showDualLineGraph(data1, data2):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    time = np.arange(0, len(data2), 1)
    plt.plot(time, data2)

    plt.show()

def printForExcel(data):
    for d in data:
        print d

def getPercCorrectPredictions(actual, predicted):
    length = min(len(actual), len(predicted)) - 1
    count = 0.0
    actualDiff = 0.0
    predictedDiff = 0.0
    for i in range(1, length):
        actualDiff = actual[i]-actual[i-1]
        predictedDiff = predicted[i]-predicted[i-1]    
        if actualDiff > 0 and predictedDiff > 0:
            count += 1.0
        elif actualDiff < 0 and predictedDiff < 0:
            count += 1.0
        else:
            continue
    return count/length


def ABGTestNetProfit(parameter):
    returns = []
    tickerList = ["F", "aapl", "ACN", "CAT", "M", "UPS", "PCLN", "CPB"]
    
    for ticker in tickerList:
        rawReadData = []
        dataPath = "./../Historical-Datal/" + ticker + ".txt"
        description.readDataFromFile(dataPath, rawReadData)
        data = description.getOpenPriceHistory(rawReadData)
    
        ta = TradingAlgorithm(data, ticker, "abg")
        totalReturn, actual, predicted = ta.run( parameter )
        returns.append(totalReturn)

    printForExcel(tickerList)
    printForExcel(returns)

def ABGTestPredVAct(parameter):
    returns = []
    ticker = "UPS"
    
    rawReadData = []
    dataPath = "./../Historical-Datal/" + ticker + ".txt"
    description.readDataFromFile(dataPath, rawReadData)
    data = description.getOpenPriceHistory(rawReadData)
    dataList.append(data)

    ta = TradingAlgorithm(data, ticker, "abg")
    totalReturn, actual, predicted = ta.run(parameter)

    # printForExcel([totalReturn])
    # print ticker
    printForExcel(actual)
    # printForExcel(predicted)
    # print getPercCorrectPredictions(actual, predicted)

def ABGTestAlpha():
    returns = []
    ticker = "UPS"
    percentCorrectList = []

    rawReadData = []
    dataPath = "./../Historical-Datal/" + ticker + ".txt"
    description.readDataFromFile(dataPath, rawReadData)
    data = description.getOpenPriceHistory(rawReadData)
    
    # Param value Generator
    params = []
    numParams = 100.0
    for i in range(1, int(numParams)):
        increment = 1.0/numParams
        params.append(i*increment)

    # params = [.05,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.90,.95]
    for p in params:
        ta = TradingAlgorithm(data, ticker, "abg")
        totalReturn, actual, predicted = ta.run(p)
        returns.append(totalReturn)
        percentCorrectList.append(getPercCorrectPredictions(actual, predicted))

    maxAlpha = params[returns.index(max(returns))]
    maxPercentCorrect = percentCorrectList[returns.index(max(returns))]

    print "Maximizing Alpha for", ticker," is", maxAlpha
    print "Realized net profit of", max(returns)
    print "Percentage Predictions Correct", maxPercentCorrect

    # printForExcel(tickerList)
    # printForExcel(returns)


dataList = []
tickerList = ["F", "aapl", "ACN", "CAT", "M", "UPS", "PCLN", "CPB"]
# tickerList = ["F"]

returns = []

for ticker in tickerList:
    rawReadData = []
    dataPath = "./../Historical-Datal/" + ticker + ".txt"
    description.readDataFromFile(dataPath, rawReadData)
    data = description.getOpenPriceHistory(rawReadData)
    dataList.append(data)

    # ---- Testing for Wiener Filter
    # ta = TradingAlgorithm(data, ticker, "Wiener")
    # totalReturn, actual, predicted = ta.run()
    # testParamReturns.append(totalReturn)

    # ---- For Testing the Double Moving Average ----
#    params = [ [25,50], [100,200] ]
#    for p in params:
#        ta = DoubleMovingAverage( data, ticker, "dma")
#        totalReturn = ta.run(p[1],p[0])
#        testParamReturns.append(totalReturn)
#        # print 'totalReturn:  ' , totalReturn

    # print "\n" + ticker 
    # printForExcel(testParamReturns)




def main():
    # Alpha Beta Gamma Tests
    # ABGTestNetProfit(0.8)
    ABGTestPredVAct(0.2)
    # ABGTestAlpha()


if __name__ == "__main__":
    main()









