
# Input
# ==========================================================================
T = float(input("Input Temp (C): "))  # Temp in Celsius
S = float(input("Input Salinity (g/kg): "))  # Salinity
L = float(input("Volume to be prepared (L): "))  # Volume in liters

# Molality (mol/Kg artificial seawater) of constituent ions
# The Molality (mol/kg) value for ions from 
# "Guide to best practices for ocean CO2 measurements"
m_Cl = 0.54922
m_SO4 = 0.02824
m_Na = 0.46911
m_Mg = 0.05283
m_Ca = 0.01036
m_K = 0.01021
m_B = 0.00042  # Assuming all boron from one source
m_CO32 = 0.0011  # Assuming carbonate contribution

# Concentration of MgCl2 & CaCl2 solutions (mol/L)
MgCl2_conc = 1.703211
CaCl2_conc = 0.952078

# ==========================================================================
# Equation of State for Seawater Density (Millero & Poisson, 1981)

# Density of pure water
rhow = (
    999.842594
    + 6.793952e-2 * T
    - 9.095290e-3 * T**2
    + 1.001685e-4 * T**3
    - 1.120083e-6 * T**4
    + 6.536332e-9 * T**5
)

# Seawater density at 1 atm (P = 0)
A = (
    8.24493e-1
    - 4.0899e-3 * T
    + 7.6438e-5 * T**2
    - 8.2467e-7 * T**3
    + 5.3875e-9 * T**4
)
B = -5.72466e-3 + 1.0227e-4 * T - 1.6546e-6 * T**2
C = 4.8314e-4

density = rhow + A * S + B * S**(3/2) + C * S**2  # kg/m³
Density = density / 1000  # kg/L

# Moles of constituent ions
Cl = m_Cl * Density * L
SO4 = m_SO4 * Density * L
Na = m_Na * Density * L
Mg = m_Mg * Density * L
Ca = m_Ca * Density * L
K = m_K * Density * L
B = m_B * Density * L
CO32 = m_CO32 * Density * L

# Molecular masses of salts
Na2SO4_mw = 142.04
KCl_mw = 74.55
NaCl_mw = 58.44
BH3O3_mw = 61.83
Na2CO3_mw = 105.99

# Boric acid to be added (g)
BH3O3 = B * BH3O3_mw
b_oh = B * 3  # Moles of B coming from BH3O3

# Na2SO4 to be added (g)
Na2SO4 = SO4 * Na2SO4_mw
sod_so4 = SO4 * 2  # Moles of Na+ from Na2SO4

# Na2CO3 to be added (g)
Na2CO3 = CO32 * Na2CO3_mw
# moles of Na+ coming from Na2CO3
sod_co32 = CO32 * 2

# KCl to be added (g)
KCl = K * KCl_mw
chlo_k = K  # Moles of Cl- from KCl

# MgCl2 solution to be added (mL)
MgCl2 = (Mg / MgCl2_conc) * 1000
chlo_mg = Mg * 2  # Moles of Cl- from MgCl2

# CaCl2 solution needed (mL)
CaCl2 = (Ca / CaCl2_conc) * 1000
chlo_ca = Ca * 2  # Moles of Cl- from CaCl2

# Na+ and Cl- from NaCl
Na_rest = Na - (sod_so4+sod_co32)
Cl_rest = Cl - (chlo_k + chlo_mg + chlo_ca)
NaCl = Na_rest * NaCl_mw

# Check balance
balance_check = Na_rest - Cl_rest

# Initial alkalinity estimate (µEq/kg)
alk = -1e6 * balance_check

# Initial DIC estimate (µM)
KH = 10**-1.46
pCO2 = 420 * 10**-6
DIC = 1e6 * m_CO32 + (KH * pCO2)

# Display results
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(f"Total Volume to be prepared (L): {L}")
print(f"Temperature (C): {T}")
print(f"Salinity (g/kg): {S}")
print()
print(f"Na2SO4 to be added (g): {Na2SO4}")
print(f'Na2CO32 to be added (g) = %f\n', Na2CO3)
print(f"BH3O3 to be added (g): {BH3O3}")
print(f"KCl to be added (g): {KCl}")
print(f"NaCl to be added (g): {NaCl}")
print(f"MgCl2 solution to be added (mL): {MgCl2}")
print(f"CaCl2 solution to be added (mL): {CaCl2}")
print(f"TA (uEq/kg): {alk}")
print(f"DIC estimate (uM): {DIC}")
print(f"Total boron estimate (uM): {1e6 * B}")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

