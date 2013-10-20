# default python
import sys
import gc
import os

# from simulation directory
import common
import equity
import investmentStrategy
import simulate

# other directories
# import read
# import test

previousData = []
futureData = []

# first render the data into a useable format
# create a folder of previous data and another of future data
# up to us to make sure data is consistent
# 
data.readDataFromFile

# get step size
stepSize = simulate.calculteStepSize(futureData)

# some simulation inputs
t0 = [ 0.01  ,  0.05  ]
t1 = [ 0.02  ,  0.075 ]
t2 = [ 0.03  ,  0.1   ]
t3 = [ 0.04  ,  0.15  ]
t4 = [ 0.05  ,  0.2   ]
t5 = [ 0.075 ,  0.3   ]
t6 = [ 0.1   ,  0.4   ]
t7 = [ 0.125 ,  0.5   ]
t8 = [ 0.15  ,  0.60  ]
t9 = [ 0.2   ,  0.75  ]

trials = [t0,t1,t2,t3,t4,t5,t6,t7,t8,t9]
results = []

for trial in trials:

    gc.collect()

    results.append( simulate.simulateTradingStrategy(previousData, futureData, stepSize, trial[0], trial[1] ) )



