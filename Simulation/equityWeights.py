import math
import datetime
import common

class EquityWeights:
    """
    EquityWeights stores the determined weight associated with each significant
    feature for an equity.
    Weights are normalized.
    The sum of all weights = 1
    Each weight is limited to [0,1]
    On initialization, all weights will have the same value
    Training will give different weights more emphasis

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
        iteratively trains from all of the data
        """

        for k in range(1, len(previousData) ):
            singleTrain( previousData[:k], previousData[k] )


    def singleTrain(self, allPreviousTicks, latestTick):
        """
        sinlgeTrain does the training for a single tick, which is 
        where all machine learning is compared across

        a tick: [ timestamp, open price, highest, lowest, close price]

        latestTick is the tick that is occurring immediately after tick
        """

        # get the current stats for the features!
        features = getFeatures(allPreviousTicks)

        # see what would be predicted from this data
        prediction = self.predict( allPreviousTicks, latestTick, features)

        # get the difference between the prediciton and the actual


    def predict(self, previousData, currentTick, features = None ):
        """
        using trained weights, predict the magnitude and direction for a change
        in stock price
        """

        # have features yet?
        if features is None:
            features = getFeatures(previousData)

        # predict sign


        # predict magnitude




