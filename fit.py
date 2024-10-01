import cbsyst as cb
import numpy as np

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




# This returns a pandas.DataFrame object with all C and B parameters.
# It also saves the data to the specified file. The extension of the
# file determined the format it is saved in (see data_out docstring).
