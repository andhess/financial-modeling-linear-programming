import common
import numpy as np
import description
from TradeAlgorithm import *
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

def showDualLineGraph(data1, data2):
    time = np.arange(0, len(data1), 1)
    plt.plot(time, data1)
    time = np.arange(0, len(data2), 1)
    plt.plot(time, data2)

    plt.show()


dataList = []
tickerList = ["F", "aapl", "ACN", "CAT", "F", "M", "UPS", "PCLN", "CPB"]
# tickerList = ["F"]

returns = []

for ticker in tickerList:
    rawReadData = []
    dataPath = "./../Historical-Datal/" + ticker + ".txt"
    description.readDataFromFile(dataPath, rawReadData)
    data = description.getOpenPriceHistory(rawReadData)
    dataList.append(data)

    ta = TradingAlgorithm(data, ticker)
    buyCount, sellCount, totalReturn, actual, predicted = ta.run()
    # print totalReturn
    returns.append(totalReturn)

print tickerList
print returns

    # # test alpha
    # params = [.05,.10,.15,.20,.25,.30,.35,.40,.45,.50,.55,.60,.65,.70,.75,.80,.85,.90,.95]
    # for p in params:
    #     ta = TradingAlgorithm(data, ticker)
    #     buyCount, sellCount, totalReturn, actual, predicted = ta.testParameter(p)
    #     print totalReturn













