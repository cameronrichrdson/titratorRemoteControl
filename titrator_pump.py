import serial
import time
import csv
import sys
from serial import Serial

# Set up the serial connection for the Arduino
arduino_ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    timeout=1
)

# Function to add progress bar in dispensing of sample
def printProgressBar(iteration, total, prefix='', suffix='', length=50):
    """
    Prints a progress bar to the terminal.

    :param iteration: Current iteration (e.g., volume dispensed)
    :param total: Total iterations (e.g., total volume)
    :param prefix: Prefix string (optional)
    :param suffix: Suffix string (optional)
    :param length: Length of the progress bar (optional)
    """
    percent = int(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = '=' * filled_length + '-' * (length - filled_length)
    sys.stdout.write(f'\r{prefix} [{bar}] {percent}% {suffix}')
    sys.stdout.flush()

# Function to send a command to the Arduino
def send_arduino_command(command):
    arduino_ser.write((command + '\r\n').encode())
    response = arduino_ser.read(arduino_ser.in_waiting).decode().strip()
    return response


#User defined inputs
acid_concentration = input("Acid concentration (mol/L): ")  # Molarity of the acid
sample_volume = input("Sample volume (mL): ")  # Volume of the sample in ml

#Dispense sample into cell
dispense_amnt = input("Please enter volume of sample to dispense into cell (mL): ")
send_arduino_command('D, -' + dispense_amnt)
print("Pump dispensing sample...")
# Example usage:

for i in range(int(dispense_amnt) + 1):
    printProgressBar(i, int(dispense_amnt), prefix='Progress:', suffix='Complete')
    time.sleep(0.01)  # Optional delay to slow down the loop (adjust as needed)

print("\nReady to begin titration")  # Indicate completion after the loop


