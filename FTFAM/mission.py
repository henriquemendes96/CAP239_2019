from aircraftData import *
from math import floor
import numpy as np


def mission(tFlight, T0, Tc0, Tf, Tcf, flashpoint):

    altitude = []
    phase = []
    engineStatus = []
    SAT = []
    TAT = []
    Ma = []

    maxFlightTime = (aircraft.get('maximumRange') - 100) * 60 / 573.6 / aircraft.get('cruiseMa') + (0.7 * 60)

    if tFlight > 240:
        tBefore = 90 # 90 minutes for long flights
    elif tFlight > 180:
        tBefore = 45 # 45 minutes for medium flights
    else:
        tBefore = 30 # 30 minutes for short flights

    tAfter = 30 # Time after flight [min]
    tMission = tBefore + tFlight + tAfter # Total mission duration [min]

    tClimb = getClimbTime(tFlight) # Climb time [min]
    tDescent = getDescentTime(tFlight) # Descent time [min]
    tCruise = tFlight - tClimb - tDescent # Cruise time[min]

    if tFlight < 50:
        alt1 = tClimb * 1750 # Climb rate of 1750 ft/min
        if alt1 > aircraft.get('cruiseAlt1'):
            alt1 = aircraft.get('cruiseAlt1') # Limits altitude at cruise altitude
        alt2 = alt1
        alt3 = alt1
        tcrz1 = 0
        tcrz2 = 0
        tcrz3 = 0
        maxCruiseAlt = alt3
    elif tFlight <= 100:
        alt1 = aircraft.get('cruiseAlt1')
        alt2 = alt1
        alt3 = alt1
        tcrz1 = tCruise
        tcrz2 = 0
        tcrz3 = 0
        maxCruiseAlt = alt3
    elif tFlight < 200: # Medium 2-step cruise flights
        alt1 = aircraft.get('cruiseAlt1')
        alt2 = aircraft.get('cruiseAlt2')
        alt3 = alt2
        tcrz1 = tCruise / 2 # Cruise time is equally split between each step
        tcrz2 = tCruise / 2
        tcrz3 = 0
        maxCruiseAlt = alt3
    else:
        alt1 = aircraft.get('cruiseAlt1')
        alt2 = aircraft.get('cruiseAlt2')
        alt3 = aircraft.get('cruiseAlt3')
        tcrz1 = tCruise / 3
        tcrz2 = tCruise / 3
        tcrz3 = tCruise / 3
        maxCruiseAlt = alt3

    ambPress = getAmbPress(maxCruiseAlt) # Gets ambient pressure table [psi]
    machTable = createMachTable(maxCruiseAlt) # Gets Mach table (Mach Vs Altitude)

    SAT_table_i, TAT_table_i = createTempTable(T0, Tc0, maxCruiseAlt, machTable) # Create initial temperature table (initial temperature vs altitude)
    SAT_table_f, TAT_table_f = createTempTable(Tf, Tcf, maxCruiseAlt, machTable) # Create final temperature table (final temperature vs altitude)

    for t in range(0, tMission, 1):
        if t < tBefore:
            altitude.append(0)
            phase.append('ground')
            if t > tBefore - aircraft.get('engineOnTimeBeforeTO'):
                engineStatus.append('on')
            else:
                engineStatus.append('off')
        elif t < round(10 * (tBefore + tClimb)) / 10:
            altitude.append(floor(alt1 * (t - tBefore) / tClimb))
            phase.append('climb')
            engineStatus.append('on')
        elif t < round(10 * (tBefore + tClimb + tcrz1)) / 10:
            altitude.append(alt1)
            phase.append('cruise1')
            engineStatus.append('on')
        elif t < round(10 * (tBefore + tClimb + tcrz1 + tcrz2)) / 10:
            altitude.append(alt2)
            phase.append('cruise2')
            engineStatus.append('on')
        elif t < round(10 * (tBefore + tClimb + tcrz1 + tcrz2 + tcrz3)) / 10:
            altitude.append(alt3)
            phase.append('cruise3')
            engineStatus.append('on')
        elif t < round(10 * (tBefore + tClimb + tcrz1 + tcrz2 + tcrz3 + tDescent) / 10):
            altitude.append(floor(alt3 - (alt3 * (t - (tBefore + tClimb + tcrz1 + tcrz2 + tcrz3)) / tDescent)))
            phase.append('descent')
            engineStatus.append('on')
        else:
            altitude.append(0)
            phase.append('taxiin')
            engineStatus.append('on')

        SAT.append(getTemp(t, tBefore + tClimb, tCruise, altitude[t], SAT_table_i, SAT_table_f, TAT_table_i, TAT_table_f, phase[t], 'SAT'))

        TAT.append(getTemp(t, tBefore + tClimb, tCruise, altitude[t], SAT_table_i, SAT_table_f, TAT_table_i, TAT_table_f, phase[t], 'TAT'))

        Ma.append(machTable[int(floor((altitude[t] + 1) / 1000))])

    mis = dict()

    mis['time'] = np.asarray(range(0, tMission, 1))
    mis['altitude'] = np.asarray(altitude)
    mis['Ma'] = np.asarray(Ma)
    mis['SAT'] = np.asarray(SAT)
    mis['TAT'] = np.asarray(TAT)
    mis['phase'] = np.asarray(phase)

    mis['SAT_iniTable'] = np.asarray(SAT_table_i)
    mis['SAT_finalTable'] = np.asarray(SAT_table_f)
    mis['TAT_iniTable'] = np.asarray(TAT_table_i)
    mis['TAT_finalTable'] = np.asarray(TAT_table_f)

    mis['engineStatus'] = np.asarray(engineStatus)

    mis['phaseTime_tBefore'] = np.asarray(tBefore)
    mis['phaseTime_tAfter'] = np.asarray(tAfter)
    mis['phaseTime_tFlight'] = np.asarray(tFlight)
    mis['phaseTime_tMission'] = np.asarray(tBefore + tAfter + tFlight)
    mis['phaseTime_tClimb'] = np.asarray(tClimb)
    mis['phaseTime_tcrz1'] = np.asarray(tcrz1)
    mis['phaseTime_tcrz2'] = np.asarray(tcrz2)
    mis['phaseTime_tcrz3'] = np.asarray(tcrz3)
    mis['phaseTime_tDescent'] = np.asarray(tDescent)

    mis['ambientPressure'] = np.asarray(ambPress)
    mis['machTable'] = np.asarray(machTable)

    mis['flashpoint'] = np.asarray(flashpoint)

    return mis


def getClimbTime(flightTime):
    # Calculating flight time for the defined aircraft maximum range (maximum flight time)
    maxFlightTime = (aircraft.get('maximumRange') - 100) * 60 / 573.6 / aircraft.get('cruiseMa') + (0.7 * 60)
    # Calculating index to access engine climb time table
    percOfFtTime = int(floor((flightTime / maxFlightTime) * 5))

    # Climb time table which relates climb time and flight time/maximum flight time, as defined by the FAA
    engineClimbTable = [[20, 20, 30, 30, 35, 35], [25, 30, 35, 35, 40, 40], [25, 35, 40, 40, 45, 50]]

    if flightTime < 50: # Exception for short flights, when climb time is 40% of the total flight time.
        clbTime = flightTime * 0.4
    else:
        clbTime = engineClimbTable[aircraft.get('nOfEngines') - 2][percOfFtTime]

    return clbTime


def getDescentTime(flightTime):
    if flightTime < 50: # Exception for short flights, when descent time is 60% of the total flight time.
        dctTime = 0.6 * flightTime
    else:
        if flightTime <= 100: # Calculates altitude at the end of cruise
            cruiseFinalAltitude = aircraft.get('cruiseAlt1') # Single altitude cruise
        elif flightTime < 200:
            cruiseFinalAltitude = aircraft.get('cruiseAlt2') # Dual altitude cruise
        else:
            cruiseFinalAltitude = aircraft.get('cruiseAlt3') # Triple altitude cruise
        # Constant descent profile for all flights. 2500 ft/min down to 4000 ft, then 500 ft / min down to the ground
        dctTime = (round(cruiseFinalAltitude / 1000) - 4) / 2.5 + 8

    return dctTime


def createTempTable(Tgrd, Tcruise, maxCruiseAlt, machTable):
    SAT_table = []
    TAT_table = []
    for alt in range(0, int(floor(maxCruiseAlt / 1000)) + 1, 1):  # Loops from altitude equal to 0
        if Tgrd > 39.9: # If temperature is more than 39.9 degF, no thermal inversion occurs
            if alt <= 9:
                SAT_table.append(Tgrd - 3.57 * alt) # Calculating the temperature for each altitude
            else:
                SAT_table.append(SAT_table[alt - 1] - 3.75)
                if SAT_table[alt] < Tcruise:
                    SAT_table.append(Tcruise)

        else: # If temperature is less than 39.9 degF, thermal inversion (temperature increases at the first layers of the atmosphere) occurs
            if alt <= 9:
                SAT_table.append(Tgrd - (Tgrd - 4.3) / 10 * alt) # Calculating the temperature for each altitude
            else:
                SAT_table.append(SAT_table[alt - 1] - 3.75)
                if SAT_table[alt] < Tcruise:
                    SAT_table.append(Tcruise)

        TAT_table.append(((SAT_table[alt] + 460) * (1 + 0.18 * machTable[alt] ** 2)) - 460) # Calculating TAT from SAT

    return SAT_table, TAT_table


def getTemp(time, tCruiseStart, tCruise, alt, SATTableIni, SATTableFinal, TATTableIni, TATTableFinal, flightPhase, whichTemp):
    if flightPhase == 'descent': # Following the FTFAM, where the rounding method at descent differs from the others
        altIndex = int(floor(alt / 1000))
    else:
        altIndex = int(floor(alt / 1000))

    if tCruise <= 120: # If total flight time is less than 120 minutes, no ground temperature change takes place
        SAT = SATTableIni[altIndex]
        TAT = TATTableIni[altIndex]
    else:
        tStartRamp = tCruiseStart + tCruise / 2 + 10 # If flight time is more than 120 minutes, the temperature changes linearly from initial temperature to final temperature 10 minutes after half of the cruise
        tEndRamp = tStartRamp + 45 # Ramp from initial to final temperature lasts 45 minutes

        if time < tStartRamp: # Before temperature change
            SAT = SATTableIni[altIndex]
            TAT = TATTableIni[altIndex]
        elif time < tEndRamp: # During temperature change - linear interpolation
            SAT = SATTableIni[altIndex] + (SATTableFinal[altIndex] - SATTableIni[altIndex]) / (tEndRamp - tStartRamp) * (time - tStartRamp)
            TAT = TATTableIni[altIndex] + (TATTableFinal[altIndex] - TATTableIni[altIndex]) / (tEndRamp - tStartRamp) * (time - tStartRamp)
        else: # After temperature change
            SAT = SATTableFinal[altIndex]
            TAT = TATTableFinal[altIndex]

    if whichTemp == 'SAT':
        return SAT
    elif whichTemp == 'TAT':
        return TAT
    else:
        return 0


def getAmbPress(maxCruiseAlt):
    ambP = []
    for alt in range(0, int(floor(maxCruiseAlt / 1000)) + 1, 1):
        ambP.append(14.7 * (1 - alt / 145.45) ** 5.2561)  # Equation relating ambient pressure with altitude, according to the FTFAM

    return ambP


def createMachTable(maxCruiseAlt):
    machTable = []
    for alt in range(0, int(floor(maxCruiseAlt / 1000)) + 1, 1):
        if alt == 0:
            machTable.append(0) # The method considers that the aircraft is always stopped on the ground
        elif alt < 10:
            machTable.append(0.4) # Mach is equal to 0.4 from 0 up to 10 kft
        elif alt < 30:
            machTable.append(((alt - 10) * (aircraft.get('cruiseMa') - 0.4) / 20) + 0.4) # Mach increases linearly up to 30 kft
        else:
            machTable.append(aircraft.get('cruiseMa')) # From 30 kft up the Ma is the cruise Mach number

    return machTable
