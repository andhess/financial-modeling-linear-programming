import math
import datetime

class DescriptionModel( object ):
    
    global learning

    """  """
    def __init__( self, data, features ):
        self.data = data

        n = len( features )
        val = 1.0 / n
        self.weights = {}

        for item in features:
            self.weights[item] = val

    def getObjectiveFunctionValue(self, time):
        """
        gets the value for existing weight values and the features currently
        observed in the model

        Input:
        time    :   the current time in the whole model
        """

        z = 0.0
        for feature in self.weights:
            z += self.weights[feature] * self.getCurrentFeature(feature, time) 

        for i in xrange(len(self.weights)):
            z += self.weights[i] * self.featureFunctions[i](time)
        return z

    def getCurrentFeature( self, feature, time ):
        """
        determine which feature function to run

        Inputs:
        time    :   the current time in the model
        feature :   the feature desired to be selected
        """

        # expand this list as more features are added
        if feature == "acceleration":
            return self.getAcceleration( time )
        elif feature == "veolocity":
            return self.getVelocity
        else:
            return 0

    def getActualReturn(self, time, endTime=0):
        """ Get the actual return of the equity by returning the difference of 
        the final price and the price at the time passed. 

        data: a list of price history
        time: the specified time 
        endTime: end time optional parameter

        examples
            data = [1,2,3,4]
            getExpectedReturn(1, 3)
            => 4-2 = 2

        """
        if endTime != 0 and time < len(self.data):
            # use the final value
            return self.data[-1] - self.data[time]
        elif endTime > time:
            # use the specified end time 
            return self.data[endTime-1] - self.data[time-1]
        else:
            # return none in case of malformed input
            return None

    def getVariance(self):
        """
        Calculate and return the variance of the data. 
        """
        return scipy.stats.variation(self.data)

    def getVelocity(self, time, span=10):
        """ Return the average velocity of the data up to time t going back 'span' units in time
            Velocity = (change in y)/(change in x)

            span: the number of points to capture the velocity for. 
            time: the time we are looking to get a slope for

        """
        # Calculate the slope using rise/run
        # print self.data
        # print self.data[time]
        # print self.data[time-span+1]
        # print span-1
        # print "results in: ", (self.data[time] - self.data[time - span + 1]) / float(span-1)


        dataSlice = []

        # get a chunk of dat with size specified by "span"
        for i in range(time - span + 1, time +1):
            if self.data[i] != None:
                dataSlice.append(self.data[i])

        # return the average of the velocities in the span
        return np.sum(np.gradient(dataSlice))/float(span)

    def getAcceleration(self, time, span=10):
        dataSlice = []

        # get a chunk of the data to calculate over
        for i in range(time - span + 1, time + 1):
            if self.data[i] != None:
                dataSlice.append(self.data[i])

        # the average acceleration
        return np.sum(np.gradient(np.gradient(dataSlice)))/float(span)

    def getFilterProjection(self, time):
        correlationList = []
        # filterLength = 2500
        for filterLength in range(500,4501,500):
            stepLen = 1
            lf = LinearFilter(self.data,filterLength,stepLen)
            expectedGains, actualGains = [], []
            for i in range(filterLength+1,len(self.data)-100):
            # for i in range(1001,1020):
                projectedValue = lf.applyFilter(i)
                expectedGain = float(projectedValue) - self.data[i]
                
                actualGain = self.data[i+1] - self.data[i]

                expectedGains.append(expectedGain)
                actualGains.append(actualGain)

            correlation = (stepLen, scipy.stats.pearsonr(expectedGains, actualGains))
            correlationList.append(correlation)
            # showDualLineGraph(expectedGains, actualGains)
            # showLineGraph(np.array(expectedGains)-np.array(actualGains))
            print correlation

        showLineGraph(np.array(correlationList))
        return (expectedGain, actualGain)

    def training( self, time ):
        
