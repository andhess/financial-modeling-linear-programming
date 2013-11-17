import math
import datetime

class EquityWeights:
    """
    EquityWeights stores the determined weight associated with each significant
    feature for an equity.
    Weights are normalized.
    The sum of all weights = 1
    Each weight is limited to [0,1]
    On initialization, all weights will have the same value
    Training will give different weights more emphasis

    This class does not do training, it just stores the weights with a feature

    Inputs: List of weights (array)
        Ex: [ "Acceleration", "Velocity", "Price", "Trend"]

    EquityWeights can accomodate as many or as little features as desired
    """

    def __init__(self, listOfWeights):
        n = len( listOfWeights )
        val = 1.0 / n

        self.signs = {}
        self.scale = {}

        for item in listOfWeights:
            self.sign[item] = val
            self.scale[item] = val

    def updateSignWeights(self, pairs):
        """
        Update the sign weights to a given value
        Able to update all or one attribute
        
        Inputs:
        pairs = [ [ <attribute name>, newValue ] , ... ]

        if just one input, will still include in array []
        """

        for pair in pairs:
            self.sign[pair[0]] = pair[1]


    def updateScaleWeights(self, pairs):
        """
        Update the scale weights to a given value
        Able to update all or one attribute      

        Inputs:
        pairs = [ [ <attribute name>, newValue ] , ... ]

        if just one input, will still include in array []
        """

        for pair in pairs:
            self.scale[pair[0]] = pair[1]

    def prevTraining(self, previousData):
        """
        prevTraining takes in an equity object and previousData

        Inputs:
        previousData  :   passed in from simulate


        previousData : [1st tick, 2nd tick, 3rd tick, .... last tick before traind period]

        each tick: [ timestamp, open price, highest, lowest, close price]

        prevTraining sets up for the 
        """

    def singleTrain(self, tick, nextTick):
        """
        sinlgeTrain does the training for a single tick


