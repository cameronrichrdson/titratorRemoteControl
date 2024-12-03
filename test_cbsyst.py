import cbsyst as cb
import numpy as np
import pandas as pd
import pymyami as py



data = {
    "ion": ["Na", "K", "Mg", "Ca", "Cl", "SO4", "CO3", "TB", "DIC", "TA"],
    "Concentration": [0.467147, 0.010248, 0.052836, 0.010366, 0.547159, 0.028319, 0.001105, 0.000417, 0.001105, 0.002209],
}

data = pd.DataFrame(data)
DIC = data.loc[data["ion"] == "DIC", "Concentration"].values[0]
TA = data.loc[data["ion"] == "TA", "Concentration"].values[0]
Mg = data.loc[data["ion"] == "Mg", "Concentration"].values[0]
Ca = data.loc[data["ion"] == "Ca", "Concentration"].values[0]
SO4 = data.loc[data["ion"] == "SO4", "Concentration"].values[0]




Csw = cb.Csys(DIC=DIC, TA=TA, Mg=Mg, Ca=Ca, Cl=Cl, SO4=SO4, T=19, )

print(Csw)