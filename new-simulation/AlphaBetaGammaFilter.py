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

    firstPoint      : The first point the data
    secondPoint     : The second point in the data
    alpha           : The estimation parameter


    Example...

    abg = AlphaBetaGammaFilter(208000.0, 207000.0, 0.41)

    rawData = [208000.0, 207000.0, 217000.0, 204000.0, 216000.0, 229000.0, 229000.0, 242000.0, 310000.0, 241000.0, 245000.0, 247000.0, 259000.0, 257000.0, 299000.0, 245000.0, 255000.0]

    should produce a projected value of 274637.135035
    
    """
    def __init__(self, firstPoint, secondPoint, alpha):
        """ Initialize the filter with model data. """
        # self.rawData = rawData
        self.predictions = []
        self.updateParameters = []

        # calculate beta and gamma based off alpha
        self.alpha = alpha
        self.beta = self.getBeta(alpha)
        self.gamma = self.getGamma(alpha, self.beta)

        # Instantiate variables since they will be used each iteration
        Xp, Vp, Residual, Xs, Vs, As =  None, None, None, None, None, None

        # Set up the initial iteration
        data = secondPoint
        Xp = self.getXp(firstPoint, 0.0, 0.0)
        Xs = secondPoint
        Vs = secondPoint - firstPoint
        As = 0.0
        Vp = 0.0

        # old self.updateParameters.append( (Xs, Vs, As) )

        self.updateParameters.append( (Xp, Vp, As) )


    def getProjectedValue(self, data):
        Xp, Vp, As = self.updateParameters[-1]

        # Smooth and update based on measurement
        residual = self.getResidual(data, Xp)
        Xs = self.getXs(Xp, residual, self.alpha)
        Vs = self.getVs(Vp, residual, self.beta)
        As = self.getAs(As, residual, self.gamma)

        # Calculate predicted values based on previous state
        Xp = self.getXp(Xs, Vs, As)
        Vp = self.getVp(Vs, As)

        self.updateParameters.append( (Xp, Vp, As) )
        self.predictions.append(Xp)
        return Xp

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



