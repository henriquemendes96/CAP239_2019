from aircraftData import *
import numpy as np

def createRangeTable(nOfFlights,ARACDistribution):
    i = 0
    pondRange = []
    cumDistributionPart = []
    cumSum = []
    cumDistribution = []

    for sRange in range(0, aircraft.get('maximumRange') + 1, 200):
        pondRange.append(ARACDistribution[i, 1] * (aircraft.get('maximumRange') - sRange))
        i = i + 1

    pondFlights = [x * nOfFlights / sum(pondRange) for x in pondRange]

    i = 0
    for sRange in range(0, aircraft.get('maximumRange') + 1, 200):
        luna = sum(pondFlights[0:i+1])
        aux = round(sum(pondFlights[0:i+1]))
        cumDistributionPart.append(round(sum(pondFlights[0:i+1])))
        i = i + 1

    cumSum.append(cumDistributionPart[0])
    i = 1

    for sRange in range(200, aircraft.get('maximumRange') + 1, 200):
        cumSum.append(cumDistributionPart[i] - cumDistributionPart[i - 1])
        i = i + 1

    percentual = [x / nOfFlights for x in cumSum]

    i = 0
    for sRange in range(0, aircraft.get('maximumRange') + 1, 200):
        cumDistribution.append(sum(percentual[0:i+1]))
        i = i + 1

    rgTableColumn1 = ARACDistribution[0:i+1, 0]
    rgTableColumn2 = [0] + cumDistribution
    rgTableColumn1 = np.asarray(rgTableColumn1)
    rgTableColumn2 = np.asarray(rgTableColumn2)
    rgTable = np.vstack((rgTableColumn1,rgTableColumn2))
    rgTable = np.transpose(rgTable)

    return rgTable
