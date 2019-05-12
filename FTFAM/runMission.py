from tankCalc import *
from aircraftData import *

def runMission(mission):
    flammTime = dict()
    time = dict()
    flammTemps = dict()

    fuelTemperatureLast = mission.get('TAT')[0]
    tank['fuelTemperature'] = []  # [degF]
    tank['tankPressure'] = []  # [psi]
    tank['tankAltitude'] = []  # [ft]
    tank['isFlammable'] = []  # [bollean]
    tank['Tlfl'] = []  # [degF]
    tank['Tufl'] = []  # [degF]
    tank['tankAlt'] = []  # [ft]
    tank['tauUsed'] = []  # [null]

    tank['tankPressure'], tank['tankAltitude'] = getTankPressure(mission)

    flammTime['total'] = 0

    for currentTime in range(-1, len(mission.get('time')) - 1, 1):
        fuelTemperature, tauUsed = getFuelTemperature(mission, currentTime, fuelTemperatureLast)
        tank.get('fuelTemperature').append(fuelTemperature)
        tank.get('tauUsed').append(tauUsed)
        fuelTemperatureLast = tank.get('fuelTemperature')[currentTime + 1]
        isFlammable = isTankFlammable(mission, currentTime)
        tank.get('isFlammable').append(isFlammable)

    tank['isFlammable'] = np.asarray(tank.get('isFlammable'))

    time['total'] = mission.get('time')[-1]
    time['climb'] = sum(mission.get('phase')=='climb')
    time['ground'] = sum(mission.get('phase')=='ground')
    time['descent'] = sum(mission.get('phase')=='descent')
    time['tcrz1'] = sum(mission.get('phase')=='cruise1')
    time['tcrz2'] = sum(mission.get('phase')=='cruise2')
    time['tcrz3'] = sum(mission.get('phase')=='cruise3')
    time['taxiin'] = sum(mission.get('phase')=='taxiin')

    flammTime['total'] = sum(tank.get('isFlammable'))
    flammTime['climb'] = sum((mission.get('phase')=='climb')*1 * tank.get('isFlammable'))
    flammTime['ground'] = sum((mission.get('phase')=='ground')*1 * tank.get('isFlammable'))
    flammTime['descent'] = sum((mission.get('phase')=='descent')*1 * tank.get('isFlammable'))
    flammTime['tcrz1'] = sum((mission.get('phase')=='cruise1')*1 * tank.get('isFlammable'))
    flammTime['tcrz2'] = sum((mission.get('phase')=='cruise2')*1 * tank.get('isFlammable'))
    flammTime['tcrz3'] = sum((mission.get('phase')=='cruise3')*1 * tank.get('isFlammable'))
    flammTime['taxiin'] = sum((mission.get('phase')=='taxiin')*1 * tank.get('isFlammable'))

    flammTemps['fuelTemperature'] = tank.get('fuelTemperature')
    flammTemps['Tlfl'] = tank.get('Tlfl')
    flammTemps['Tufl'] = tank.get('Tufl')

    return time, flammTime, flammTemps