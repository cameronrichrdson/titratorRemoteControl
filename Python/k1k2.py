import numpy as np
import pandas as pd

# Given values
T_celsius = 10
S = 34.943
T_kelvin = T_celsius + 273.15


############################# Roy1993 on sw scale######################
# Components of the equation
S_sqrt = np.sqrt(S)
S_15 = S * S_sqrt

roy_pK1 = -np.log10(np.exp((3.17537 - (2329.1378 / T_kelvin) - 1.597015 * np.log(T_kelvin) +
         (-0.210502 - (5.79495 / T_kelvin)) * S_sqrt +
         0.0872208 * S - 0.00684651 * S_15)))

roy_pK2 = -np.log10(np.exp((-8.19754 - (3403.8782 / T_kelvin) - 0.352253 * np.log(T_kelvin) +
         (-0.088885 - (25.95316 / T_kelvin)) * S_sqrt +
         0.1106658 * S - 0.00840155 * S_15)))

############################ Goyet and Poisson 1989 on sw scale ########################

GP_pK1 = 807.18 / T_kelvin + 3.374 - 0.00175 * S * np.log(T_kelvin) + 0.000095 * S ** 2
GP_pK2 = 1486.6 / T_kelvin + 4.491 - 0.00412 * S * np.log(T_kelvin) + 0.000215 * S ** 2

############################## Millero 2006 #########################

#pK1
A1 = 13.4191 * np.sqrt(S) + 0.0331 * S - 5.33e-5 * S ** 2
B1 = -530.123 * np.sqrt(S) - 6.103 * S
C1 = -2.06950 * np.sqrt(S)

pK1_0 = -126.34048 + 6320.813 / T_kelvin + 19.568224 * np.log(T_kelvin)
millero_pK1 = A1 +(B1/T_kelvin) + C1*np.log(T_kelvin) + pK1_0

A2 = 21.0894 * np.sqrt(S) + 0.1248 * S - 3.687e-4 * S ** 2
B2 = -772.483 * np.sqrt(S) - 20.051 * S
C2 = -3.3336 * np.sqrt(S)

pK2_0 = -90.18333 + 5143.692 / T_kelvin + 14.613358 * np.log(T_kelvin)
millero_pK2 = A2 +(B2/T_kelvin) + C2*np.log(T_kelvin) + pK2_0


########################################## Mojica and Millero 2002 ####################################################


mojica_pK1 = -43.6977 - 0.0129037*S + 1.364e-4*(S**2) + 2885.378/T_kelvin + 7.045159*np.log(T_kelvin)

mojica_pK2 = -452.0940 + 13.142162*S - 8.101e-4*(S**2) + 21263.61/T_kelvin + 68.483143*np.log(T_kelvin) + (-581.4428*S + 0.259601*(S**2))/T_kelvin - (1.967035*S)*np.log(T_kelvin)



#################################### Lueker 2000 ########################################################################
lueker_pK1 = 3633.86/T_kelvin - 61.2172 + 9.67770*np.log(T_kelvin) - 0.011555*S +0.0001152*(S**2)
lueker_pK2 = 471.78/T_kelvin +25.9290-3.16967*np.log(T_kelvin) -0.01781*S + 0.0001122*(S**2)


#######



########################################## Millero 1995, Roy 1993 and GP 1989 combined (sw scale)####################################################


combined_pK1 = -np.log10(np.exp(2.18867-2275.0360/T_kelvin - 1.468591*np.log(T_kelvin) + (-0.138681-9.33291/T_kelvin)*(np.sqrt(S)) +0.0726483*S - 0.00574938*S**1.5))
combined_pK2 = -np.log10(np.exp(-0.84226 + -3741.1288/T_kelvin + -1.437139*np.log(T_kelvin)  + ((-0.128417 - 24.41239/T_kelvin)*(np.sqrt(S))) + (0.1195308*S) + (-0.00912840*S**1.5)))

#######

########################################## Dickson and Millero 1989, Hansson and Mehrbach combined refit on pH(SWS) ####################################################


########## ONLY FOR SALINITY RANGE OF 20 <= S <= 40
combined_pK1_DM = (845/T_kelvin)+3.248-0.0098*S+0.000087*(S**2)
combined_pK2_DM = (1377.3/T_kelvin)+4.824-0.0185*S+0.000122*(S**2)


####################################################################################millero roy 1997
# a_millero = -60.2409
# b_millero = -9345.17
# c_millero = 18.7533
 
# k_millero197 = np.exp(a_millero + b_millero/T_kelvin + c_millero*np.log(T_kelvin))


print("~~~~~~~~~~~~~~~~~~~~~~~~~", "\n", "T (C) = ", T_celsius, "\n", "S (g/kg)= ", S, "\n","~~~~~~~~~~~~~~~~~~~~~~~~~")
print(" Using Roy1993 formulation (asw):")
print(" pK1 = ", roy_pK1, "\n", "pK2 = ", roy_pK2, "\n")
print(" Using Goyet & Poisson 1989 formulation (asw):")
print(" pK1 = ", GP_pK1, "\n", "pK2 = ", GP_pK2, "\n")
print(" Using Millero 2006 formulation :")
print(" pK1 = ", millero_pK1, "\n", "pK2 = ", millero_pK2, "\n")
print(" Using Mojica & Millero 2002 formulation (sw):")
print(" pK1 = ", mojica_pK1, "\n", "pK2 = ", mojica_pK2, "\n")
print(" Using Lueker 2000 formulation (sw):")
print(" pK1 = ", lueker_pK1, "\n", "pK2 = ", lueker_pK2, "\n")
print(" Millero 1995, Roy 1993 and GP 1989 combined (asw):")
print(" pK1 = ", combined_pK1, "\n", "pK2 = ", combined_pK2, "\n")
print(" Dickson and Millero 1989, Hansson and Mehrbach combined refit on pH(SWS):")
print(" pK1 = ", combined_pK1_DM, "\n", "pK2 = ", combined_pK2_DM, "\n")
# print(" Millero 1997:", k_millero197)


# data = {
#     "Formulation": ["Roy1993", "Goyet & Poisson 1989", "Millero 2006", "Mojica & Millero 2002", "Lueker 2000", "Millero 1995, Roy 1993 and GP 1989 combined", "Dickson and Millero 1989, Hansson and Mehrbach combined refit"],
#     "Author": ["ROY93", "GP89", "MILL06", "MM02", "LUEK00", "MRG95", "DM89"],
#     "pK1": [roy_pK1, GP_pK1, millero_pK1, mojica_pK1, lueker_pK1, combined_pK1, combined_pK1_DM],
#     "pK2": [roy_pK2, GP_pK2, millero_pK2, mojica_pK2, lueker_pK2, combined_pK2, combined_pK2_DM]
# }

# df = pd.DataFrame(data)
# filename = f"S{S}_T{T_celsius}_pKvalues.csv"
# df.to_csv(f'/Users/cameronrichardson/Documents/GitHub/titratorRemoteControl/Python/{filename}', index=False)
# print(filename, "has been saved to the current working directory.")