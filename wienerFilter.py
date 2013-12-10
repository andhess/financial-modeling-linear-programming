import numpy as np
import scipy as sc
#import matplotlib as plt
import random
import time
import math
from operator import itemgetter

# to test the wienerFilter, open python in terminal and paste these commands

# import read
# import wienerFilter
# data = []
# read.readDataFromFile('./Historical-Datal/fb.txt', data)
# del data[0]
# test = wienerFilter.WienerPredictor(data)
# test.filter(10,4,"heuristic")



class WienerPredictor():
    """ An implementation of the wiener filter. """
    def __init__(self, data):
        self.data = data

    def filter(self, time, steps, method, noise=False, sigma=1):
        
        self.steps = steps
        self.sigma = sigma
        self.time = time
        self.setNoise(noise)

        
        w = self.getW(method)

        prediction = 0
        print 'w  : ' , w

        for i in range(steps):
            print (time-i)
            prediction += w[i] * ( self.data[time-i][1] + self.noise[time-i] )

        return prediction

    def getW(self, method):

        if method == "matrices":
            Rx = self.constructRx()
            rdx = self.constructrdx()
            w = Rx.i * rdx
            w = w.tolist()

            return [ i[0] for i in w ]

        elif method == "heuristic":
            return self.wMinErrorHueristic()

        elif method == "brute":
            return self.wMinErrorBrute(100)

        elif method == "superBrute":
            return self.wMinErrorBrute(10000)

        elif method == "bruteAlt":
            return self.wMinErrorBruteAlt(100)

        elif method == "superBruteAlt":
            return self.wMinErrorBruteAlt(10000)

        else:
            raise Exception()

    def wMinErrorBruteAlt(self, precision):
        t = self.time - self.steps
        alpha = [0] * self.steps
        
        for i in range(self.steps):

            error = [0] * (precision + 1)
            for j in range(precision + 1):

                predict = 0
                for l in range(self.steps):
                    predict += (1.0 * j)/precision * (self.data[t+i-l][1] + self.noise[i-l])

                error[j] = math.pow( ( ( self.data[t+i+1][1] ) - predict ) , 2)

            alpha[i] = ( 1.0 * min( enumerate(error), key=itemgetter(1))[0] ) / precision

        return alpha



    def wMinErrorBrute(self, precision):
        t = self.time - self.steps
        alpha = [0] * self.steps
        
        for i in range(self.steps):

            error = [0] * (precision + 1)
            for j in range(precision + 1):

                predict = 0
                for l in range(i):
                    predict += alpha[l] * (self.data[t+i-l][1] + self.noise[i-l])

                predict += (1.0 * j)/precision * (self.data[t][1] + self.noise[0])
                error[j] = math.pow( ( ( self.data[t+i+1][1] ) - predict ) , 2)

            alpha[i] = ( 1.0 * min( enumerate(error), key=itemgetter(1))[0] ) / precision

        return alpha


    def wMinErrorHueristic(self):
        t = self.time - self.steps
        alpha = [0] * self.steps

        print 'time:  ' , self.time
        print 't:  ' , t
        print 'alpha:  ' , alpha
        print 'noise:  ' , self.noise
        
        for i in range(self.steps):

            error = [0] * 11
            for j in range(11):

                predict = 0
                for l in range(i):
                    predict += alpha[l] * (self.data[t+i-l][1] + self.noise[i-l])

                predict += j/10.0 * (self.data[t][1] + self.noise[0])
                error[j] = math.pow( ( ( self.data[t+i+1][1] ) - predict ) , 2)

            min1 = min( enumerate(error), key=itemgetter(1))[0]
            print 'error:  ' , error

            error2 = [0] * 21
            for k in range(21):

                predict = 0
                for l in range(i):
                    predict += alpha[l] * (self.data[t+i-l][1] + self.noise[i-l] )

                predict += ( min1/10.0 + (k - 11)/100.0) * (self.data[t][1] + self.noise[0])
                error2[k] = math.pow( ( ( self.data[t+i+1][1] ) - predict ) , 2)

            print 'error2:  ' , error2
            min2 = min( enumerate(error2), key=itemgetter(1))[0]

            alpha[i] = min1/10.0 + (min2 - 11)/100.0
            print 'alpha:  ' , alpha[i]
            print alpha
            print '----------'

        return alpha

    def constructRx(self):
        pass

    def constructrdx(self):
        pass

    def setNoise(self, nType):
        noise = []
        if nType == "white":
            for i in range(len(self.data)):
                noise.append( random.gauss(0, self.sigma) )
        else:
            for i in range(len(self.data)):
                noise.append( 0 )

        self.noise = noise