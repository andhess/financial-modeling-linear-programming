
class investmentStrategy:
    """
    investmentStrategy keeps track of every position held over time
    """

    def __init__( self, availableCapital ):

        self.liquid = [availableCapital]
        self.positions = {}
        self.value = []

    def addInstrument( self, instrument ):
        """
        add an instrument to the investmentStrategy

        Input:
        instrument  :   the instrument being added
        """

        self.positions[instrument] = []

    def recordPosition(self, instrumentSymbol, value, numPositions ):
        """
        records the position on given instrument 

        Input:
        value           :   the current value of the 
        numPositions    :   the number of positions held on instrument
        """

        info = [value, numPositions]
        self.positions[instrumentSymbol].append( info )

    def calculateValue(self):
        """
        Calculates the current value of all assets, frozen and liquid
        """

        amount = self.liquid[-1]
        for data in self.positions
            amount += data[-1][0]*data[-1][1]

        self.value.append(amount)

    