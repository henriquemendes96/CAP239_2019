from math import gcd
import random
import numpy as np
import scipy.stats as st

'''
The probability that two random numbers sharing a common factor is 
6/(pi^2). These number are called coprimes. Numbers that do share 
a common factor are called cofactors. The number one does not count.
Reference: https://www.youtube.com/watch?v=RZBhSi_PwHU
'''

# ============================ Inputs ============================
# Total of trials
total = 0
# Number of Monte Carlo simulations
trials = 100
# Total of times the two random number do not share a factor
coprime = 0
# Number of "dice rolls"
simulations = 100
# Random numbers will vary between zero and maxRandom
maxRandom = 1000

results = []
# Every trial is a different Monte Carlo simulation.
for tri in range(trials):
    # For all simulations
    for sim in range(simulations):
        # Random numbers form a normal distribution
        n1 = random.randint(1, maxRandom)
        n2 = random.randint(1, maxRandom)
        # If the GCD is 1, then the numbers are coprime
        if gcd(n1, n2) == 1:
            coprime += 1.0
        total += 1
    # Just compiles the results of every trial
    results.append((6/(coprime/total))**0.5)

# Every result of each trial will be approximately equal to pi
print(np.mean(results))
print(st.t.interval(0.95, len(results)-1, loc=np.mean(results), scale=st.sem(results)))
