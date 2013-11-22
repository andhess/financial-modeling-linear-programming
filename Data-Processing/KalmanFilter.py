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

ab = AlphaBetaFilter([0])
ab.execute()
        