import numpy as np

class AlphaBetaGammaFilter():
    """
    The AlphaBetaGammaFilter is an estimator with close similarities to the Kalman Filter
    and other linear state observers used in Control Theory. Its advantage is that it does
    not require a detailed system model. 

    It assumes that the system can be adequately approximated by making predictions based on
    the model's current and previous states. It performs remarkably well for simple linear
    systems, and it has been shown to perform modestly in estimating some more complex systems.  

    ________________Parameters________________

    rawData         :       The model data to estimate
    alpha           :       The estimation parameter - optimal value to be determined experimentally. 


    Example...

    rawData = [208000.0, 207000.0, 217000.0, 204000.0, 216000.0, 229000.0, 229000.0, 242000.0, 310000.0, 241000.0, 245000.0, 247000.0, 259000.0, 257000.0, 299000.0, 245000.0, 255000.0]

    should produce a projected value of 274637.135035
    
    """
    def __init__(self, rawData):
        """ Initialize the filter with model data. """
        self.rawData = rawData

    def getProjectedValue(self, alpha):
        # calculate beta and gamma based off alpha
        beta = self.getBeta(alpha)
        gamma = self.getGamma(alpha, beta)

        # Uncomment to record all predicted values 
        actualValues = []
        predictedValues = []

        # Instantiate variables since they will be used each iteration
        Xp, Vp, Residual, Xs, Vs, As =  None, None, None, None, None, None

        # Set up the initial iteration
        data = self.rawData[1]
        Xp = self.getXp(self.rawData[0], 0.0, 0.0)
        Xs = self.rawData[1]
        Vs = self.rawData[1] - self.rawData[0]
        As = 0.0

        # Run the algorithm to find the projected value
        for i in range(2, len(self.rawData)):
            # Calculate predicted values based on previous state
            Xp = self.getXp(Xs, Vs, As)
            Vp = self.getVp(Vs, As)

            # Smooth and update based on measurement
            data = self.rawData[i]
            residual = self.getResidual(data, Xp)
            Xs = self.getXs(Xp, residual, alpha)
            Vs = self.getVs(Vp, residual, beta)
            As = self.getAs(As, residual, gamma)

            # Uncomment to store predicted values
            predictedValues.append(Xp)
            actualValues.append(data)
    
        # Get the final projected value based on calculated values
        Xp = self.getXp(Xs, Vs, As)

        # Uncomment to return all predicted values. Note, don't store the predictedValues 
        # array since self.rawData and predictedValues will be different sizes. 
        # print predictedValues
        return (actualValues, predictedValues)
        # return predictedValues

        # print Xp
        # return Xp

    def getXp(self, Xs_minus, Vs_minus, As_minus):
        """ Calculate Xp for the AlphaBetaGamma Algorithm """
        return Xs_minus + Vs_minus + 0.5*As_minus

    def getVp(self, Vs_minus, As_minus):
        """ Calculate Vp for the AlphaBetaGamma Algorithm """
        return Vs_minus + As_minus

    def getResidual(self, data, Xp):
        """ Calculate residual for the AlphaBetaGamma Algorithm """
        return data - Xp

    def getXs(self, Xp, residual, alpha):
        """ Calculate Xs for the AlphaBetaGamma Algorithm """
        return Xp + alpha*residual

    def getVs(self, Vp, residual, beta):
        """ Calculate Vs for the AlphaBetaGamma Algorithm """
        return Vp + beta*residual

    def getAs(self, As_minus, residual, gamma):
        """ Calculate As for the AlphaBetaGamma Algorithm """
        return As_minus + gamma*residual

    def getBeta(self, alpha):
        """ Calculate Beta for the AlphaBetaGamma Algorithm """
        return 2.0*(2.0-alpha) + -4.0*np.sqrt(1.0-alpha)

    def getGamma(self, alpha, beta):
        """ Calculate Gamma for the AlphaBetaGamma Algorithm """
        return np.power(beta,2.0)/2.0/alpha



