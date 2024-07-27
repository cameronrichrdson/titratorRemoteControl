import serial
import time
import csv
import sys
from serial import Serial

# Set up the serial connection for the titrator
titrator_ser = serial.Serial(
    port='COM5',
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=1
)

# Set up the serial connection for the Arduino
arduino_ser = serial.Serial(
    port='COM4',
    baudrate=9600,
    timeout=1
)


# Function to send a command and read the response from the titrator
def send_titrator_command(command):
    titrator_ser.write((command + '\r\n').encode())
    time.sleep(0.1)
    response = titrator_ser.read(titrator_ser.in_waiting).decode().strip()
    return response

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

# Initialize the titrator and prepare it for dosing
send_titrator_command('$L(DOS)')  # Load the dosing method
send_titrator_command('$G')  # Start the method

# Prepare to log data
log_file = 'titrator_log.csv'
fields = ['Time', 'Acid Volume Dosed (ml)', 'Acid Concentration (M)', 'Sample Volume (ml)']
data = []

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



try:
    while True:


        # Trigger a dosing step
        send_titrator_command('$G')

        # Get the dosed volume
        dosed_volume = send_titrator_command('$Q(VOLUME)')

        # Record the data
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data.append([timestamp, dosed_volume, acid_concentration, sample_volume])

        # Log the data to a CSV file
        with open(log_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(fields)
            writer.writerows(data)

        print(f"Dosed {dosed_volume} ml of acid at {timestamp}")

        # Wait before the next dose (adjust as needed for your application)
        time.sleep(60)

        flush = input("Flush sample from cell? (yes/no)")
        if flush() == "yes":
            send_arduino_command('D, ' + dispense_amnt)
        elif flush() == "no":
            print("Standing by...")
        else:
            print("Type 'yes' or 'no'")


finally:
    titrator_ser.close()
    arduino_ser.close()

