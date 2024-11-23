import numpy as np

# Given values
T_celsius = 19
# S = 35.050462
S = 34.8
T_kelvin = T_celsius + 273.15


############################# Roy1993 ######################
# Components of the equation
ln_T = np.log(T_kelvin)
S_sqrt = np.sqrt(S)
S_15 = S * S_sqrt

roy_pK1 = -np.log10(np.exp((2.83655 - (2307.1266 / T_kelvin) - 1.552941 * ln_T +
         (-0.20760841 - (4.0484 / T_kelvin)) * S_sqrt +
         0.08468345 * S - 0.00654208 * S_15)))

roy_pK2 = -np.log10(np.exp((-9.226508 - (3351.6106 / T_kelvin) - 0.200574 * ln_T +
         (-0.106901773 - (23.9722 / T_kelvin)) * S_sqrt +
         0.1130822 * S - 0.00846934 * S_15)))

############################ Goyet and Poisson 1989########################

GP_pK1 = 812.27 / T_kelvin + 3.356 - 0.00171 * S * np.log(T_kelvin) + 0.000091 * S ** 2
GP_pK2 = 1450.87 / T_kelvin + 4.604 - 0.00385 * S * np.log(T_kelvin) + 0.000182 * S**2

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

############################## Mehrbach 1973 ###########################
#for t= 19, s= 35
mehr_pK1 = 6.03245202378
mhr_pK2 = 9.1951793213


########################################## Mojica and Millero 2002 ####################################################


mojica_pK1 = -43.6977 - 0.0129037*S + 1.364e-4**S + 2885.378/T_kelvin + 7.045159*np.log(T_kelvin)

mojica_pK2 = -452.0940 + 13.142162*S - 8.101e-4**S + 21263.61/T_kelvin + 68.483143*np.log(T_kelvin) + (-581.4428*S + 0.259601**S)/T_kelvin - (1.967035*S)*np.log(T_kelvin)



#################################### Lueker 2000 ########################################################################
lueker_pK1 = 3633.86/T_kelvin - 61.2172 + 9.67770*np.log(T_kelvin) - 0.011555*S +0.0001152**S
lueker_pK2 = 471.78/T_kelvin +25.9290-3.16967*np.log(T_kelvin) -0.01781*S + 0.0001122**S


#######



########################################## Millero 1995, Roy 1993 and GP 1989 combined ####################################################


combined_pK1 = -np.log10(np.exp(2.18867-2275.0360/T_kelvin - 1.468591*np.log(T_kelvin) + (-0.138681-9.33291/T_kelvin)*(np.sqrt(S)) +0.0726483*S - 0.00574938*S**1.5))
combined_pK2 = -np.log10(np.exp(-0.84226 + -3741.1288/T_kelvin + -1.437139*np.log(T_kelvin)  + ((-0.128417 - 24.41239/T_kelvin)*(np.sqrt(S))) + (0.1195308*S) + (-0.00912840*S**1.5)))

#######


print("~~~~~~~~~~~~~~~~~~~~~~~~~", "\n", "T (C) = ", T_celsius, "\n", "S (g/kg)= ", S, "\n","~~~~~~~~~~~~~~~~~~~~~~~~~")
print(" Using Roy1993 formulation (asw):")
print(" pK1 = ", roy_pK1, "\n", "pK2 = ", roy_pK2, "\n")
print(" Using Goyet & Poisson 1989 formulation (asw):")
print(" pK1 = ", GP_pK1, "\n", "pK2 = ", GP_pK2, "\n")
print(" Using Millero 2006 formulation :")
print(" pK1 = ", millero_pK1, "\n", "pK2 = ", millero_pK2, "\n")
print(" Using Mehrbach 1973 formulation (sw):")
print(" pK1 = ", mehr_pK1, "\n", "pK2 = ", mhr_pK2, "\n")
print(" Using Mojica & Millero 2002 formulation (sw):")
print(" pK1 = ", mojica_pK1, "\n", "pK2 = ", mojica_pK2, "\n")
print(" Using Lueker 2000 formulation (sw):")
print(" pK1 = ", lueker_pK1, "\n", "pK2 = ", lueker_pK2, "\n")
print(" Millero 1995, Roy 1993 and GP 1989 combined (asw):")
print(" pK1 = ", combined_pK1, "\n", "pK2 = ", combined_pK2, "\n")