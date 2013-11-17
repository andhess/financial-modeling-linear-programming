import math
import datetime



def training(equitySymbol, data):



def readDataFromFile(fileName, outputList):
    # open the file from bloomberg

    fl = open(fileName, "r")

    # ignore the first line
    #fl.readline()

    for i, line in enumerate(fl):

        entry = []

        if line.startswith("Symbol"):
            name = line.replace("\t", " ").replace("\r\n", "").split(" ")
            outputList.append(name[1])
            continue

        elif line.startswith("Date"):
            continue

        elif line.startswith("\r\n"):
            continue

        line = line.replace("\t", " ").replace("\r\n", "")

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

        entry.append((timestamp, openPrice, highPrice, lowPrice, closePrice))

#        if len(snapshot) > 6:
#            tradeVolume = int(snapshot[6])
#            entry.append(tradeVolume)

        # Store tuple of snapshot data in list
        outputList.append(entry)

    fl.close()

