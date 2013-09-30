import numpy, scipy.stats

def describe(data):
    """
    Describe the data passed
    - mean
    """
    print scipy.stats.describe(data)
    return scipy.stats.describe(data)

