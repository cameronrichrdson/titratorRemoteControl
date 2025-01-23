import test_cbsyst as cb
import numpy as np

# Constants
MAX = 100
MA = 4
SPREAD = 0.001
V0 = 212.1947
NR_END = 1
FREE_ARG = str
IA = 16807
IM = 2147483647
AM = (1.0 / IM)
IQ = 127773
IR = 2836
NTAB1 = 32
NDIV = (1 + (IM - 1) // NTAB1)
EPS1 = 1.0e-4
EPS2 = 1.2E-7
RNMX = (1.0 - EPS2)
CON = 1.4
CON2 = (CON * CON)
BIG = 1.0e30
NTAB2 = 10
SAFE = 2.0

# Custom seawater composition
custom_composition = {
    'Mg': 0.0528171,  # mol/kg
    'Ca': 0.0102821,  # mol/kg
    'Na': 0.468,      # mol/kg
    'Cl': 0.54586,    # mol/kg
    'SO4': 0.0282352, # mol/kg
    'CO3': 0.00234,   # mol/kg
    'K': 0.010207,    # mol/kg
    'Boric acid': 0.000416, # mol/kg
}

def cnst(consts, custom_composition):
    T = consts[14] + 273.15
    t = consts[14]
    sal = consts[15]
    sqrts = np.sqrt(sal)
    I = 19.92 * sal / (1000 - 1.005 * sal)

    consts[1] = np.log(10) * 8.31441 * T / 96484.56
    consts[2] = custom_composition['Boric acid']
    consts[3] = custom_composition['SO4']
    consts[4] = 0.000067 / 18.9984 * (sal / 1.80655)
    ks = np.exp((-4276.1 / T + 141.328 - 23.093 * np.log(T) + (-13856 / T + 324.57 - 47.986 * np.log(T)) * np.sqrt(I) + (35474 / T - 771.54 + 114.723 * np.log(T)) * I - 2698 / T * I * np.sqrt(I) + 1776 / T * I * I) + np.log(1 - sal * 0.001005))
    consts[5] = ks
    kf = np.exp(1590.2 / T - 12.641 + 1.525 * np.sqrt(I) + np.log(1 - sal * 0.001005))
    consts[6] = kf
    z = 1 + custom_composition['SO4'] / ks + custom_composition['Boric acid'] / kf
    consts[7] = z
    consts[8] = np.exp((-8966.90 - 2890.53 * sqrts - 77.942 * sal + 1.728 * sal * sqrts - 0.0996 * sal * sal) / T + (148.0248 + 137.1942 * sqrts + 1.62142 * sal) + (-24.4344 - 25.085 * sqrts - 0.2474 * sal) * np.log(T) + 0.053105 * sqrts * T + np.log((1 + custom_composition['SO4'] / ks + custom_composition['Boric acid'] / kf) / (1 + custom_composition['SO4'] / ks)))
    consts[9] = np.exp(-13847.26 / T + 148.96502 - 23.6521 * np.log(T) + (118.67 / T - 5.977 + 1.0495 * np.log(T)) * sqrts - 0.01615 * sal)
    consts[13] = np.exp(3.17537 - 2329.1378 / T - 1.597015 * np.log(T) + (-0.210502 - 5.79495 / T) * sqrts + 0.0872208 * sal - 0.00684651 * sal * sqrts)
    consts[12] = np.exp(-(1394.7 / T + 4.777 - 0.0184 * sal + 0.000118 * sal * sal) * np.log(10))
    a = 8.24493e-4 - 4.0899e-6 * t + 7.6438e-8 * t * t - 8.2467e-10 * t * t * t + 5.3875e-12 * t * t * t * t
    b = -5.72466e-6 + 1.0227e-7 * t - 1.6546e-9 * t * t
    c0 = 4.8314e-7
    d0 = 0.999842594 + 6.793953e-5 * t - 9.09529e-6 * t * t + 1.001685e-7 * t * t * t - 1.120083e-9 * t * t * t * t + 6.536332e-12 * t * t * t * t * t
    consts[10] = d0 + a * sal + b * sal * sqrts + c0 * sal * sal
    na = 0.7 - consts[16]
    h = consts[16]
    cl = 0.7
    I0 = (na + cl + h) / 2
    E = (na + cl + h) / 2
    na = na / E
    cl = cl / E
    h = h / E
    M = na * 22.9898 + cl * 35.453 + h * 1.008
    nacl = (45.5655 - .2341 * t + 0.0034128 * t * t - 2.703e-5 * t * t * t + 1.4037e-7 * t * t * t * t) * I0 + (-1.8527 + 0.053956 * t - 6.2635e-4 * t * t) * I0 * np.sqrt(I0) + (-1.6368 - 9.5653e-4 * t + 5.2829e-5 * t * t) * I0 * I0 + 0.2274 * I0 * I0 * np.sqrt(I0)
    nacl = (nacl / 1000) + d0
    phinacl = 1000 * (d0 - nacl) / (I0 * nacl * d0) + (22.9898 + 35.453) / nacl
    hcl = (20.3368 - 0.0737834 * t - 5.29257e-3 * t * t + 4.50398e-4 * t * t * t - 1.17417e-5 * t * t * t * t + 1.02433e-7 * t * t * t * t * t) * I0 - 1.46902 * I0 * np.sqrt(I0)
    hcl = hcl / 1000 + d0
    phihcl = 1000 * (d0 - hcl) / (I0 * hcl * d0) + (1.008 + 35.453) / hcl
    pna = phinacl * na * cl
    ph = h * cl * phihcl
    phimix = pna + ph
    consts[11] = (M * E + 1000) * d0 * (1 / (phimix * E * d0 + 1000))

# Create pH master variable for demo
pH = np.linspace(7,11,100)  # pH on Total scale

# Example Usage
# -------------
# The following functions can be used to calculate the
# speciation of C and B in seawater, and the isotope
# fractionation of B, given minimal input parameters.
#
# See the docstring for each function for info on
# required minimal parameters.

# Carbon system only
Csw = cb.Csys(pHtot=pH, DIC=2000.)

# Boron system only
Bsw = cb.Bsys(pHtot=pH, BT=433., dBT=39.5)

# Carbon and Boron systems
CBsw = cb.CBsys(pHtot=pH, DIC=1100., BT=433., dBT=39.5)

# NOTE:
# At present, each function call can only be used to
# calculate a single minimal-parameter combination -
# i.e. you can't pass it multiple arrays of parameters
# with different combinations of parameters, as in
# the Matlab CO2SYS code.

# Example Output
# --------------
# The functions return a Bunch (modified dict with '.'
# attribute access) containing all system parameters
# and constants.
#
# Output for a single input condition shown for clarity:

out = cb.CBsys(pHtot=8.1, DIC=2000., BT=433., dBT=39.5)
out
# All of the calculated output arrays will be the same length as the longest
# input array.

# Access individual parameters by:
out.CO3

# Example usage
consts = np.zeros(18)
consts[14] = 25  # Example temperature in Celsius
consts[15] = 35  # Example salinity
consts[16] = 0.01  # Example acid concentration
cnst(consts, custom_composition)
print(consts)

# This returns a pandas.DataFrame object with all C and B parameters.
# It also saves the data to the specified file. The extension of the
# file determined the format it is saved in (see data_out docstring).
