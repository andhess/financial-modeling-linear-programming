import numpy as np

class LinearFilter():
    """docstring for LinearFilter
    A linear filter in the form S*K = R
    where S is our stimulant
    K is our filter
    and R is the desired outcome

    """
    def __init__(self, data, filterLength=1000, stepLength=10):
        self.data = data
        self.s, self.r = self.buildSystem(filterLength, stepLength)
        self.filterLength = filterLength
        self.k = self.getFilter(self.s,self.r) 

    def getFilter(self, s, r):
        sInv = np.linalg.pinv(s)
        k = sInv*r
        return k       

    def buildSystem(self, filterLength, stepLength):
        """
        Build the system for a linear filter K in the equation S*K=R
        S is formed by gathering discrete slices of data at a constant rate
        across the data. 

        take data = [10,13,15,17,12,10,...]
        S = [10, 13, 15, 17
             13, 15, 17, 12
             15, 17, 12, 10
                        ... ]

        with a step rate of 1. 

        For each slice, take the next value and store it in R. For row 1 of S above, 
        take 12 for R1. 
        R = [12
             10
                ...]

        then the K, which is a solution of this equation, can be applied to any row in S
        to get its corresponding value in R. 

        this K can then be applied to any chunk of data of the same length in the data set. 
        the result will be an estimate of the value coming directly after that chunk in the data. 

    
        Implementation: 

        At each iteration, take a chunk of data of length = filterLength. 
        Store this chunk as a row in the matrix. Each iteration should move
        forward by a number of steps specified by stepLength. 

        Result with step = 1: 
        S = [10, 13, 15, 17;
             13, 15, 17, 12
             15, 17, 12, 10
                        ... ]

        """

        print "building system with filterLength =",filterLength, "and step length =", stepLength

        if stepLength > filterLength:
            print "Step length must be less than the filter length"
            return (None,None)

        # stimulants
        sMatrix = []
        # desired response
        rMatrix = []

        # up to the first filterlength is the first iteration, then we add the 
        # remaining length of data divided by the stepLength. Subtract 1 though b/c
        # we need to account for capturing the desired next step for the rMatrix. 
        numberOfIterations = int( (len(self.data) - filterLength - 1) / stepLength)

        chunk = []
        currentIndex = filterLength

        for k in range(filterLength):
            chunk.append(self.data[k])

        sMatrix.append(chunk)
        rMatrix.append([self.data[currentIndex]])

        for i in range(numberOfIterations):
            # move the chunk forward by stepLength
            chunk = chunk[stepLength:]
            for j in range(stepLength):
                chunk.append(self.data[currentIndex + j])

            # capture the chunk
            sMatrix.append(chunk)

            currentIndex += stepLength

            # capture the desired next value
            rMatrix.append([self.data[currentIndex]])


        s = np.matrix(sMatrix)
        r = np.matrix(rMatrix)
        return (s,r)


    def applyFilter(self, time):
        if time < self.filterLength:
            print "Time must be greater than the filterLength"
            return None

        # print "applying filter at time t=",time
        # print s
        chunk = []
        for i in range(self.filterLength):
            chunk.append(self.data[time + 1 - self.filterLength + i])
        chunk = np.matrix(chunk)

        expectedValue = chunk * self.k
        return expectedValue


# lf = LinearFilter([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20])
# print lf.applyFilter(12, 12)


