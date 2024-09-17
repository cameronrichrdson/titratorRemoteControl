import os
import pandas as pd

# Set the working directory

dir = os.chdir('/Users/cameronrichardson/Documents/School/Thesis/Code/titrations/')

files_in_dir = os.listdir()
print("Files in directory:", files_in_dir, "\n")

import pandas as pd

# Define the file name
file_name = 'titration_data.05a'

# Create an empty DataFrame for the initial data
columns_initial = ['Acid m (mol/kg)', 'Cell Vol (ml)', 'Cell T (oC)']
df_initial = pd.DataFrame(columns=columns_initial)

# Prompt the user for initial entries
acid_m = float(input("Enter value for 'Acid m (mol/kg)': "))
cell_vol = float(input("Enter value for 'Cell Vol (ml)': "))
cell_t = float(input("Enter value for 'Cell T (oC)': "))

# Add initial data to the DataFrame
initial_row = pd.DataFrame([{'Acid m (mol/kg)': acid_m, 'Cell Vol (ml)': cell_vol, 'Cell T (oC)': cell_t}])

# Write the initial data and the salinity line to the file
with open(file_name, 'w') as file:
    # Write the header with leading space
    file.write(" Acid m (mol/kg), Cell Vol (ml), Cell T (oC)\n")

    # Write the initial data with leading space
    for index, row in initial_row.iterrows():
        file.write(f" {row['Acid m (mol/kg)']:.1f}, {row['Cell Vol (ml)']:.1f}, {row['Cell T (oC)']:.3f}\n")

    # Write the salinity line without leading space
    file.write("Salinity = 35.000\n")

# Start a counter for entries
entry_counter = 0

# Prompt the user for mV and V entries
while True:
    try:
        # Get volume and mV values
        volume = float(input("Enter volume (mL): "))
        mv = float(input("Enter mV value: "))

        # Prepare the new entry as a string with the desired format
        entry_str = f"{entry_counter}, {volume:.3f}, {mv:.3f}\n"

        # Append the new entry to the file
        with open(file_name, 'a') as file:
            file.write(entry_str)

        print("Entry added!\n")

        # Increment the counter
        entry_counter += 1

    except ValueError:
        done = input("Are you finished entering data? Type 'yes' to finish or 'no' to continue: ")
        if done.lower() == 'yes':
            break

print(f"Data entry complete! The titration data is saved in {file_name}.")