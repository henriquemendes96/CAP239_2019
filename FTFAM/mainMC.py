from mission import *
import matplotlib.pyplot as plt
from createRangeTable import createRangeTable
from getMissionInputs import *
from runMission import *
from collections import OrderedDict

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

def main():
    timeFleet = dict()
    flammTimeFleet = dict()
    fleetPercent = dict()

    timeFleet['total'] = 0
    timeFleet['ground'] = 0
    timeFleet['climb'] = 0
    timeFleet['tcrz1'] = 0
    timeFleet['tcrz2'] = 0
    timeFleet['tcrz3'] = 0
    timeFleet['descent'] = 0
    timeFleet['taxiin'] = 0

    flammTimeFleet['total'] = 0
    flammTimeFleet['ground'] = 0
    flammTimeFleet['climb'] = 0
    flammTimeFleet['tcrz1'] = 0
    flammTimeFleet['tcrz2'] = 0
    flammTimeFleet['tcrz3'] = 0
    flammTimeFleet['descent'] = 0
    flammTimeFleet['taxiin'] = 0

    fleetPercent['total'] = 0
    fleetPercent['ground'] = 0
    fleetPercent['climb'] = 0
    fleetPercent['tcrz1'] = 0
    fleetPercent['tcrz2'] = 0
    fleetPercent['tcrz3'] = 0
    fleetPercent['descent'] = 0
    fleetPercent['taxiin'] = 0

    df = np.loadtxt('C:\Users\Dell\Documents\INPE\CAP239\Python\ARACDistribution.txt')

    nOfFlights = 1000
    rgtable = createRangeTable(nOfFlights,df)

    flashPoint = []
    SAT_i = []
    SAT_f = []
    SAT_c_i = []
    SAT_c_f = []
    tFlight = []

    for n in range(0, nOfFlights, 1):

        fp, SATi, SATci, SATf, SATcf, timeFlight = getMissionInputs(rgtable)

        flashPoint.append(fp)
        SAT_i.append(SATi)
        SAT_c_i.append(SATci)
        SAT_f.append(SATf)
        SAT_c_f.append(SATcf)
        tFlight.append(int(timeFlight))

        mis = mission(tFlight[n], SAT_i[n], SAT_c_i[n], SAT_f[n], SAT_c_f[n], flashPoint[n])

        time, flammTime, flammTemps = runMission(mis)

        timeFleet['total'] = timeFleet.get('total') + time.get('total')
        timeFleet['climb'] = timeFleet.get('climb') + time.get('climb')
        timeFleet['ground'] = timeFleet.get('ground') + time.get('ground')
        timeFleet['descent'] = timeFleet.get('descent') + time.get('descent')
        timeFleet['tcrz1'] = timeFleet.get('tcrz1') + time.get('tcrz1')
        timeFleet['tcrz2'] = timeFleet.get('tcrz2') + time.get('tcrz2')
        timeFleet['tcrz3'] = timeFleet.get('tcrz3') + time.get('tcrz3')
        timeFleet['taxiin'] = timeFleet.get('taxiin') + time.get('taxiin')

        flammTimeFleet['total'] = flammTimeFleet.get('total') + flammTime.get('total')
        flammTimeFleet['climb'] = flammTimeFleet.get('climb') + flammTime.get('climb')
        flammTimeFleet['ground'] = flammTimeFleet.get('ground') + flammTime.get('ground')
        flammTimeFleet['descent'] = flammTimeFleet.get('descent') + flammTime.get('descent')
        flammTimeFleet['tcrz1'] = flammTimeFleet.get('tcrz1') + flammTime.get('tcrz1')
        flammTimeFleet['tcrz2'] = flammTimeFleet.get('tcrz2') + flammTime.get('tcrz2')
        flammTimeFleet['tcrz3'] = flammTimeFleet.get('tcrz3') + flammTime.get('tcrz3')
        flammTimeFleet['taxiin'] = flammTimeFleet.get('taxiin') + flammTime.get('taxiin')

    fleetPercent['total'] = round(float(flammTimeFleet.get('total')) / timeFleet.get('total'),4) * 100
    fleetPercent['climb'] = round(float(flammTimeFleet.get('climb')) / timeFleet.get('climb'),4) * 100
    fleetPercent['ground'] = round(float(flammTimeFleet.get('ground')) / timeFleet.get('ground'),4) * 100
    fleetPercent['descent'] = round(float(flammTimeFleet.get('descent')) / timeFleet.get('descent'),4) * 100
    fleetPercent['tcrz1'] = round(float(flammTimeFleet.get('tcrz1')) / timeFleet.get('tcrz1'),4) * 100
    fleetPercent['tcrz2'] = round(float(flammTimeFleet.get('tcrz2')) / timeFleet.get('tcrz2'),4) * 100
    fleetPercent['tcrz3'] = round(float(flammTimeFleet.get('tcrz3')) / timeFleet.get('tcrz3'),4) * 100
    fleetPercent['taxiin'] = round(float(flammTimeFleet.get('taxiin')) / timeFleet.get('taxiin'),4) * 100

    keyorder = {k: v for v, k in enumerate(['ground', 'climb', 'tcrz1', 'tcrz2', 'tcrz3', 'descent', 'taxiin', 'total'])}
    timeFleet = OrderedDict(sorted(timeFleet.items(), key=lambda i: keyorder.get(i[0])))

    print "{:<10} {:<12} {:<15} {:<15}".format('Phase', 'Time [min]', 'Flammable [min]', 'Percent')
    for key, value in timeFleet.iteritems():
        valueIterTime = value
        valueIterFlamm = flammTimeFleet.get(key)
        valueIterPercent = fleetPercent.get(key)
        if key != 'total':
            print "{:<10} {:<12} {:<15} {:<15}".format(key, valueIterTime, valueIterFlamm, valueIterPercent)
        else:
            print "{:<14} {:<12} {:<15} {:<15}".format(color.BOLD + key,str(valueIterTime), str(valueIterFlamm), str(valueIterPercent) + color.END)

if __name__ == '__main__':
    main()
