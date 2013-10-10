import numpy, scipy.stats

def describe(data):
    """
    Describe the data passed
    - mean
    """
    print scipy.stats.describe(data)
    return scipy.stats.describe(data)

def getOpenPriceHistory(data):
    """
    Given an array of tuples in the form: (Date, Open, High, Low, Close, Volume)
    return a list of the openPrices.  
    """
    priceHistory = list()
    
    for snapshot in data:
        openPrice = snapshot[1]
        priceHistory.append(openPrice)

    return priceHistory

def beta(dataA, dataB):
    """
    -correlated volatility of/ financial elasticity

    Beta-A your = Convariance( Ra , Rb ) / Variance( Rb )

    Ra = rate of return of a
    Rb = rate of return of b (benchmark)

    B < 0  - moves in the opposite direction as compared to the index
    B = 0  - movement is uncorrelated with the movement of the benchmark
    B > 0  - movement is in same direction as benchmark, about same amount as benchmark
    B > 1  - moves in same direction as benchmark, but by more value
    """

# def delta(


# # def rateOfReturn():


