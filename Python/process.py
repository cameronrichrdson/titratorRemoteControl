#init packages

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def process(file_path):
    d = pd.read_csv(file_path)
    d = d.iloc[:, -2:]
    d.rename(columns={d.columns[0]: 'mV', d.columns[1]: 'dose'}, inplace=True)
    d = d[d['dose'] != 99]
    d['dose'] = d['dose'].iloc[::-1].reset_index(drop=True)
    d['mV'] = d['mV'].round(3)

    acid = 0
    acid += 0.05 if d['dose'].iloc[-1] == 1 else 0
    d['hcl'] = d['dose'].cumsum() * 0.05
    output_file_path = '/Users/cameronrichardson/Documents/Thesis/Code/data/Salinity/~$S0212C3N04.csv'
    # d = d[d['dose'] != 0]
    d.to_csv(output_file_path, index=False)
    print(d)

 

# Example usage
# Call the function with the file path
# process('/Users/cameronrichardson/Desktop/0203C01N01.csv')


process('/Users/cameronrichardson/Documents/Thesis/Code/data/Salinity/VOLTAGE0212C03N04.csv')


