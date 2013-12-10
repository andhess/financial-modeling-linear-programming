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
#tickerList = ["PEP", "aapl", "ACN", "CAT", "F", "M", "UPS", "PCLN", "CPB"]
tickerList = ["F"]

for ticker in tickerList:
    rawReadData = []
    dataPath = "./../Historical-Datal/" + ticker + ".txt"
    description.readDataFromFile(dataPath, rawReadData)
    data = description.getOpenPriceHistory(rawReadData)
    dataList.append(data)

ta = TradingAlgorithm(dataList, tickerList)
ta.run()
