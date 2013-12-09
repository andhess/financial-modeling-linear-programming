import numpy as np
import scipy as sc
import matplotlib as plt
import random
import time

class WienerPredictor():
    """ An implementation of the wiener filter. """
    def __init__(self, data):
        self.data = data

    def filter(self, time, steps, noise=False, sigma=1, method):
        
        self.steps = steps
        self.sigma = sigma
        self.time = time
        self.setNoise(noise)

        
        w = self.getW(method)

        prediction = 0

        for i in range(steps):
            prediction += w[i] * self.data[time-i]

        return prediction

    def getW(self, method):

        if method == 1:
            Rx = self.constructRx()
            rdx = self.constructrdx()
            w = Rx.i * rdx
            w = w.tolist()

            return [ i[0] for i in w ]

        else:

            wMinError()

    def wMinError(self):




    def constructRx(self):


    def constructrdx(self):




    def setNoise(self, nType):
        noise = []
        if nType == "white":
            for i in range(self.steps):
                noise.append( random.gauss(0, self.sigma) )
        else:
            for i in range(self.steps):
                noise.append( 0 )

        self.noise = noise