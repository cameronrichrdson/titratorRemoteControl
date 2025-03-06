import os
import pandas as pd

# Set the working directory

dir = os.chdir('C:\Richardson')

files_in_dir = os.listdir()
print("Files in directory:", files_in_dir, "\n")

# Define the file name
file_name = input("Enter file name: ")

# Create an empty DataFrame for the initial data
columns_initial = ['Acid m (mol/kg)', 'Cell W (g)', 'Cell T (oC)']
df_initial = pd.DataFrame(columns=columns_initial)

# Prompt the user for initial entries
acid_m = float(input("Enter value for 'Acid m (mol/kg)': "))
cell_vol = float(input("Enter value for 'Cell W (g)': "))
cell_t = float(input("Enter value for 'Cell T (oC)': "))

# Add initial data to the DataFrame
initial_row = pd.DataFrame([{'Acid m (mol/kg)': acid_m, 'Cell W (g)': cell_vol, 'Cell T (oC)': cell_t}])

# Write the initial data and the salinity line to the file
with open(file_name, 'w') as file:
    # Write the header with leading space
    file.write(" Acid m (mol/kg), Cell W (g), Cell T (oC)\n")

    # Write the initial data with leading space
    for index, row in initial_row.iterrows():
        file.write(f" {row['Acid m (mol/kg)']}, {row['Cell W (g)']}, {row['Cell T (oC)']:.3f}\n")

    # Write the salinity line without leading space
    file.write("Salinity = 35.000\n")

# Start a counter for entries and initialize cumulative volume
entry_counter = 0
cumulative_volume = 0.0

# Prompt the user for mV and volume entries
while True:
    try:
        # Get volume increment and mV values
        volume_increment = float(input("Enter volume increment (mL): "))
        mv = float(input("Enter mV value: "))

        # Update the cumulative volume
        cumulative_volume += volume_increment

        # Prepare the new entry as a string with the desired format
        entry_str = f" {entry_counter}, {cumulative_volume}, {mv}\n"

        # Append the new entry to the file
        with open(file_name, 'a') as file:
            file.write(entry_str)

        print("Entry: ", entry_counter, "added!\n")
        # Increment the counter
        entry_counter += 1

    except ValueError:
        # If the user types 'done', break the loop
        done = input("Are you finished entering data? Type 'yes' to finish or 'no' to continue: ")
        if done.lower() == 'yes':
            break

print(f"Data entry complete! The titration data is saved in {file_name}.")


