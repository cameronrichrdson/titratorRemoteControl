import numpy as np

# Given values
T_celsius = 25
S = 35
T_kelvin = T_celsius + 273.15

# Components of the equation
ln_T = np.log(T_kelvin)
S_sqrt = np.sqrt(S)
S_15 = S * S_sqrt

# Equation for ln(K1,K2) from Roy1993
ln_K1 = (2.83655 - (2307.1266 / T_kelvin) - 1.552941 * ln_T +
         (-0.20760841 - (4.0484 / T_kelvin)) * S_sqrt +
         0.08468345 * S - 0.00654208 * S_15)

ln_K2 = (-9.226508 - (3351.6106 / T_kelvin) - 0.200574 * ln_T +
         (-0.106901773 - (23.9722 / T_kelvin)) * S_sqrt +
         0.1130822 * S - 0.00846934 * S_15)

K1 = np.exp(ln_K1)
K2 = np.exp(ln_K2)
pK1 = -np.log10(K1)
pK2 = -np.log10(K2)

print(" pK1 = ", pK1, "\n", "pK2 = ", pK2)


