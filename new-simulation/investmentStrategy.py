
class investmentStrategy:
    """
    investmentStrategy keeps track of every position held over time
    It also serves as the manager be
    """

    def __init__( self, availableCapital ):

        self.liquid = availableCapital
        self.positions = {}

    def addInstrument( self, instrument ):
        self.positions[instrument] = []

    def recordPositions(self, equities):
        timePosition = []

        for i, equity in enumerate(equities):

            if self.equityPositions[0] is not equity.symbol:
                raise Exception("Symbol matrix doesn't match up")

            timePosition.append([equity.currentValue, equity.numPositions])

        self.equityPositions.append(timePosition)
        
