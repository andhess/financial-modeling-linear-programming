import datetime

"""
    Insert tuples of the instrument's price fluctuations into 
    the specified list
"""
def readDataFromFile(fileName, outputList):
    # open the file from bloomberg
    fl = open(fileName, "r")

    # ignore the first line
    fl.readline()

    for line in fl:
        snapshot = line.split(" ")
        
        # get date and time of snapshot
        dateComponents = snapshot[0].split("-")
        year = int(dateComponents[0])
        month = int(dateComponents[1])
        day = int(dateComponents[2])

        timeComponents = snapshot[1].split(":")
        hour = int(timeComponents[0])
        minute = int(timeComponents[1])
        second = int(timeComponents[2])

        timestamp = datetime.datetime(year, month, day, hour, minute, second)

        # Get financial data
        openPrice = float(snapshot[2])
        highPrice = float(snapshot[3])
        lowPrice = float(snapshot[4])
        closePrice = float(snapshot[5])

        tradeVolume = int(snapshot[6])

        # Store tuple of snapshot data in list
        outputList.append((timestamp, openPrice, highPrice, lowPrice, closePrice, tradeVolume))

    fl.close()
