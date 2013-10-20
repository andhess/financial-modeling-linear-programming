
class investmentStrategy:
    """
    investmentStrategy keeps track of every position held over time
    It also serves as the manager be
    """

    def __init__(self, availableCapital, equities):

        self.liquid = availableCapital
        self.equityPositions = []

        for instrument in equities:
            equity = [instrument, []]
            self.equityPositions.append(equity)

