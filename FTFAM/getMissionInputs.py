from aircraftData import *
from random import uniform
from scipy.stats import norm

def getMissionInputs(rangeTable):
    product = 0
    while product == 0: # The norminv function is undefined for input equal to 0. This if condition gets new random numbers when that happened
        rnd_fp = uniform(0, 1)
        rnd_sat_i = uniform(0, 1)
        rnd_sat_f = uniform(0, 1)
        rnd_sat_ci = uniform(0, 1)
        rnd_sat_fi = uniform(0, 1)
        rnd_rg = uniform(0, 1)
        product = rnd_fp * rnd_sat_i * rnd_sat_f * rnd_sat_ci * rnd_sat_fi * rnd_rg  # Analysis if at least one of the random number is 0

    # Flashpoint from distribution
    flashPoint = norm.ppf(rnd_fp, loc=120, scale=8) # Flashpoint from FTFAM normal distribution (mean = 120 degF, std = 8 degF)
    # SAT from distributions
    SAT_i = getGroundSAT(rnd_sat_i) # Initial ground SAT
    SAT_f = getGroundSAT(rnd_sat_f) # Final ground SAT
    SAT_c_i = norm.ppf(rnd_sat_ci, loc=-70, scale=8) # Initial cruise SAT from FTFAM normal distribution (mean = -70 degF, std = 8 degF)
    SAT_c_f = norm.ppf(rnd_sat_fi, loc=-70, scale=8) # Final cruise SAT from FTFAM normal distribution(mean = -70 degF, std = 8 degF)

    # Evaluating if ambient temperature is higher then the OAT cutoff temperature
    if SAT_i > aircraft.get('OATcutoff'):
        SAT_i = aircraft['OATcutoff']

    # Flight range
    rg = getRange(rnd_rg, rangeTable)

    # Calculates flight time for the determined range
    flightTime = (rg - 100) * 60 / 573.6 / aircraft.get('cruiseMa') + (0.7 * 60)
    flightTime = round(flightTime)
    maxFlightTime = (aircraft.get('maximumRange') - 100) * 60 / 573.6 / aircraft.get('cruiseMa') + (0.7 * 60)
    if flightTime < 15:  # Limits minimum flight time at 15 minutes.
        flightTime = 15
    elif flightTime > maxFlightTime:
        flightTime = maxFlightTime

    return flashPoint, SAT_i, SAT_c_i, SAT_f, SAT_c_f, flightTime


def getGroundSAT(rnd):
    if rnd < 0.5:  # FTFAM temperature distribution is an assymetric normal distribution (different std before and after 0.5)
        SAT = norm.ppf(rnd, loc=59.94568382, scale=20.13778676) # Ground SAT from FTFAM lower normal distribution (mean=59.94568382 degF, std=20.13778676 degF)
    else:
        SAT = norm.ppf(rnd, loc=59.94568382, scale=17.27959602) # Ground SAT from FTFAM lower normal distribution (mean=59.94568382 degF, std=17.27959602 degF)

    return SAT

def getRange(rnd_rg,rangeTable):
    for i in range(0, len(rangeTable), 1): # Goes through the range table until the cumulative distribution is equal to the input random number
        if rangeTable[i + 1, 1] > rnd_rg and rangeTable[i, 1] < rnd_rg:
            flyRange = (rangeTable[i + 1, 0] + (rangeTable[i + 1, 0] - rangeTable[i, 0]) /
                        (rangeTable[i + 1, 1] - rangeTable[i, 1]) * (rnd_rg - rangeTable[i + 1, 1]))
            break
    return flyRange