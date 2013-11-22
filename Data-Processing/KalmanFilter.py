import numpy as np
import scipy as sc
import matplotlib as plt
import random
import time

class KalmanFilter():
    """ An implementation of the kalman filter. """
    def __init__(self, data):
        this.data = data


    def buildSystem():
        """" The Kalman Filter requires the initial state, phi, H, Q and R. """
        # x1 = ?
        # x2 = ?
        # x = np.matrix([[x1],[x2]])
        # sigma = ?

        A = np.matrix([ [0,1],[0,0] ])
        B = np.matrix([ [0],[sigma] ])




class AlphaBetaFilter():
    """docstring for AlphaBetaFilter"""
    def __init__(self, data):
        self.data = data

    def filter(self, alpha):
        beta = 
        gamma = 

        filteredData = []

        rawData = [208000.0, 207000.0, 217000.0, 204000.0, 216000.0, 229000.0, 229000.0, 242000.0, 310000.0, 241000.0, 245000.0, 247000.0, 259000.0, 257000.0, 299000.0, 245000.0, 255000.0]

        Xp = None
        Vp = None
        Residual = None
        Xs = None
        Vs = None
        As = None

        Xs_0 = rawData[0]

        data = rawData[1]
        Xp = self.getXp(Xs_0, 0.0, 0.0)
        Xs = rawData[1]
        Vs = rawData[1] - rawData[0]
        As = 0.0

        filteredData.append(Xs)

        for i in range(2, len(rawData)):
            print "Iteration:", i
            data = rawData[i]
            print data
            Xp = self.getXp(Xs, Vs, As)
            print "Xp", Xp
            Vp = self.getVp(Vs, As)
            print "Vp:", Vp
            residual = self.getResidual(data, Xp)
            print "Residual", residual

            Xs = self.getXs(Xp, residual, alpha)
            print "Xs", Xs
            Vs = self.getVs(Vp, residual, beta)
            print "Vs", Vs
            As = self.getAs(As, residual, gamma)
            print "As", As
            print "\n"

            filteredData.append(Xs)

        # for i in range(min(len(filteredData), len(rawData))):
        #     print "Raw:", rawData[i], " | ", filteredData[i], " :FilteredData"

    def getXp(self, Xs_minus, Vs_minus, As_minus):
        return Xs_minus + Vs_minus + 0.5*As_minus

    def getVp(self, Vs_minus, As_minus):
        return Vs_minus + As_minus

    def getResidual(self, data, Xp):
        return data - Xp

    def getXs(self, Xp, residual, alpha):
        return Xp + alpha*residual

    def getVs(self, Vp, residual, beta):
        return Vp + beta*residual

    def getAs(self, As_minus, residual, gamma):
        return As_minus + gamma*residual

    def execute(self):
        dt = 0.5
        xk_1 = 0
        vk_1 = 0
        a = 0.85
        b = 0.005

        xk = None
        vk = None   
        rk = None   
        xm = None   

        while( 1 ):
            xm = random.sample(xrange(10000), 1)[0] % 100 # random signal

            xk = xk_1 + ( vk_1 * dt )
            vk = vk_1

            rk = xm - xk

            xk += a * rk
            vk += ( b * rk ) / dt

            xk_1 = xk
            vk_1 = vk

            print( "%f \t %f\n", xm, xk_1 )
            time.sleep( 1 )

ab = AlphaBetaFilter([1])
ab.filter(0.2)        






