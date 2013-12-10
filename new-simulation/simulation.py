import common
# import portolioItem
# import investmentStrategy
import description
from TradeAlgorithm import *


rawReadData = []
ticker = "PEP"
dataPath = "./../Historical-Datal/" + ticker + ".txt"
description.readDataFromFile(dataPath, rawReadData)
data = description.getOpenPriceHistory(rawReadData)

ta = TradingAlgorithm(data)
ta.run()
