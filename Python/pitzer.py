import pytzer as pz
from collections import OrderedDict
from pytzer.libraries import Millero98

# Define the total moralities of each component (example values)
totals = OrderedDict({
    "CO2": 0.002,   # total carbonate species
    "SO4": 0.028,   # total sulfate species
    "BOH3": 0.0004, # total borate species
    "Mg": 0.052,    # total magnesium species
    "Ca": 0.0103,   # total calcium species
})

# params = Millero98.get_parameters(solutes=totals, temperature=298.15, pressure=10.1023, verbose=True
# )
#
# Gibbs_nRT = pz.model.Gibbs_nRT(totals, params)
# Gibbs_nRT = pz.Gibbs_nRT(totals, params)


# Solve the equilibrium solution
solutes, pks_constants = pz.solve(
    totals=totals,
    exclude_equilibria=None,  # if you want to exclude any equilibria
    ks_constants=None,        # if you want to provide your own initial guesses for constants
    ks_only=None,             # if you want to keep some constants fixed
    library=Millero98,         # use the Seawater library for parameters
    pressure=10.10325,        # pressure in dbar (example: 10.10325 dbar)
    temperature=298.15,       # temperature in Kelvin (example: 298.15 K)
    verbose=False             # set to True for detailed output
)

# Display the results
print("Equilibrium solutes at thermodynamic equilibrium:")
for solute, molality in solutes.items():
    print(f"{solute}: {molality:.6f} mol/kg")

print("\nEquilibrium constants (pKs):")
for equilibrium, pks in pks_constants.items():
    print(f"{equilibrium}: {pks:.6f}")
