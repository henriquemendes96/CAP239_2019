from aircraftData import *
import math
import numpy as np

def tankCalc(mission):

    tank['fuelTemperature'] = [] # [degF]
    tank['tankPressure'] = [] # [psi]
    tank['tankAltitude'] = [] # [ft]
    tank['isFlammable'] = [] # [bollean]
    tank['Tlfl'] = [] # [degF]
    tank['Tufl'] = [] # [degF]
    tank['tankAlt'] = [] # [ft]
    tank['tauUsed'] = [] # [null]

    tank['tankPressure'], tank['tankAltitude'] = getTankPressure(mission)

    return tank

def getTankPressure(mission):
    x = 1.4 / (1.4 - 1)
    tankPress = ((mission.get('ambientPressure') * (1 + 0.2 * mission.get('machTable') ** 2) ** x) - mission.get('ambientPressure')) * (aircraft.get('NACARecoveryEfficiency') / 100) + mission.get('ambientPressure')
    tankAltitude = ((1 - (tankPress / 14.7) ** (1 / 5.2561)) * 145.45) * 1000
    return tankPress, tankAltitude

def getFuelTemperature(mission, currentTime, fuelTemperatureLast):
    timeLeft = mission.get('phaseTime_tMission') - currentTime # Time left for the mission to end

    if timeLeft > (tank.get('minimumTankFullTime') + mission.get('phaseTime_tAfter')): # Is tank full?
        if mission.get('engineStatus')[currentTime + 1] == 'on': # Are engines on?
            tauGround = tank.get('engineOn_fullTau')
        else:
            tauGround = tank.get('engineOff_fullTau')
        tauFlight = tank.get('flight_fullTau')

    if timeLeft <= (tank.get('maximumTankEmptyTime') + mission.get('phaseTime_tAfter')): # Is tank empty?
        if mission.get('engineStatus')[currentTime + 1] == 'on': # Are engines on?
            tauGround = tank.get('engineOn_emptyTau')
        else:
            tauGround = tank.get('engineOff_emptyTau')
        tauFlight = tank.get('flight_emptyTau')

    targetTemperatureFlight = tank.get('flight_deltaT') # Flight temperature delta

    if mission.get('engineStatus')[currentTime + 1] == 'on':
        tconstFull = tank.get('engineOn_fullTau')
        tconstEmpty = tank.get('engineOn_emptyTau')
        targetTemperatureGround = tank.get('engineOn_deltaT')
    else:
        tconstFull = tank.get('engineOff_fullTau')
        tconstEmpty = tank.get('engineOff_emptyTau')
        targetTemperatureGround = tank.get('engineOff_deltaT')

    if (tank.get('maximumTankEmptyTime') + mission.get('phaseTime_tAfter')) < timeLeft <= (tank.get('minimumTankFullTime') + mission.get('phaseTime_tAfter')):
        tauGround = (((timeLeft - (tank.get('maximumTankEmptyTime') + mission.get('phaseTime_tAfter')))
                     / (tank.get('minimumTankFullTime') - tank.get('maximumTankEmptyTime'))) * (tconstFull - tconstEmpty) + tconstEmpty)
        tauFlight = (((timeLeft - (tank.get('maximumTankEmptyTime') + mission.get('phaseTime_tAfter')))
                     / (tank.get('minimumTankFullTime') - tank.get('maximumTankEmptyTime')))
                    * (tank.get('flight_fullTau') - tank.get('flight_emptyTau')) + tank.get('flight_emptyTau'))

    lapseRateGround = (1 - math.exp(-1 / tauGround))
    lapseRateFlight = (1 - math.exp(-1 / tauFlight))

    if mission.get('phase')[currentTime + 1] == 'ground':
        steptemp = (mission.get('TAT')[currentTime + 1] + targetTemperatureGround) - fuelTemperatureLast
        fuelTemp = fuelTemperatureLast + steptemp * lapseRateGround
        tauInUse = tauGround
    else:
        steptemp = (mission.get('TAT')[currentTime + 1] + targetTemperatureFlight) - fuelTemperatureLast
        fuelTemp = fuelTemperatureLast + steptemp * lapseRateFlight
        tauInUse = tauFlight

    return fuelTemp, tauInUse


def isTankFlammable(mission, currentTime):
    if currentTime <= (mission.get('phaseTime_tBefore') - tank.get('pressTimeBeforeTO')):
        tank['tankAlt'].append(mission.get('altitude')[currentTime + 1])
    else:
        tank['tankAlt'].append(tank.get('tankAltitude')[int(math.floor(mission.get('altitude')[currentTime + 1] / 1000))])

    tank['Tlfl'].append((mission.get('flashpoint') - 10) - tank.get('tankAlt')[currentTime + 1] / 808)
    tank['Tufl'].append((mission.get('flashpoint') + 63.5) - tank.get('tankAlt')[currentTime + 1] / 512)

    if tank.get('fuelTemperature')[currentTime + 1] > tank.get('Tlfl')[currentTime + 1]:
        isFlammable = 1
    else:
        isFlammable = 0
    if tank.get('fuelTemperature')[currentTime + 1] > tank.get('Tufl')[currentTime + 1]:
        isFlammable = 0

    return isFlammable
