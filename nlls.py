import numpy as np
from scipy.optimize import curve_fit


# Model function F(xi, P), where P = [V0, TCO2, E0, K1_prime, K2_prime]
def titration_model(x, V0, TCO2, E0, K1_prime, K2_prime):
    # The equation for titration curve fitting
    # Customize based on the specific titration model.
    # x is typically the difference of potential (mV or pH)
    # and y is the volume of acid added.

    # Example equation using some simplified form
    # of proton equivalent balance equation:
    HCO3_conc = K1_prime * x / (V0 + x)
    CO3_conc = K2_prime * x / (V0 + x)
    OH_conc = 1e-7  # for simplicity, can be dynamic
    H_conc = 1e-7  # for simplicity, can be dynamic

    return V0 * (HCO3_conc + 2 * CO3_conc + OH_conc - H_conc)


# Residual sum of squares function to minimize (S = sum((F(xi, P) - yi)^2))
def residuals(params, x, y):
    V0, TCO2, E0, K1_prime, K2_prime = params
    y_model = titration_model(x, V0, TCO2, E0, K1_prime, K2_prime)
    return np.sum((y - y_model) ** 2)


# Experimental data (xi is potential difference, yi is acid volume)
def perform_curve_fitting(x_data, y_data):
    # Initial guess for parameters (V0, TCO2, E0, K1_prime, K2_prime)
    initial_guess = [0.001, 0.002, 0.01, 10**-5.84, 10**-8.9]

    # Fit the curve using non-linear least squares (Levenberg-Marquardt)
    popt, pcov = curve_fit(titration_model, x_data, y_data, p0=initial_guess)

    # popt contains the optimized parameters V0, TCO2, E0, K1_prime, K2_prime
    # pcov is the covariance of the parameters
    return popt, pcov


# Example of titration data points (difference of potential xi and volume of acid added yi)
# You would replace this with actual titration data
# Example potentials
x_data = np.array([-119.4,-106.3,-89.2,-62.3,-1.6,7.1,14.3,20.5,25.9,30.9,35.5,39.8,43.9,47.9,51.7,
                   55.5,59.3,63.2,67.1,80.6,98.7,106.5,116.2,128.4,142.6,156.2,166.9,175.1,181.5])

y_data = np.array([0.0, 0.5, 1.0, 1.5, 2.0,2.1,2.2,2.3,2.4,2.5,2.6,2.7,2.8,
                  2.9,3.0,3.1,3.2,3.3,3.4,3.7,4.0,4.1,4.2,4.3,4.4,4.5,4.6,4.7,4.8])


# Perform the curve fitting
optimized_params, covariance = perform_curve_fitting(x_data, y_data)

# Display the optimized parameters
V0, TCO2, E0, K1_prime, K2_prime = optimized_params
print(f"Optimized Parameters:\nV0 = {V0}\nTCO2 = {TCO2}\nE0 = {E0}\nK1' = {K1_prime}\nK2' = {K2_prime}")

# Optionally, you can calculate the statistical errors (standard deviation of the parameters)
parameter_errors = np.sqrt(np.diag(covariance))
print(f"Parameter Errors:\n{parameter_errors}")
