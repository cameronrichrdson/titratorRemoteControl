import serial
import time
import csv

# Set up the serial connection for the titrator
titrator_ser = serial.Serial(
    port='COM2',  # Replace with your actual COM port for the titrator
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=1
)

# Set up the serial connection for the Arduino
arduino_ser = serial.Serial(
    port='COM3',  # Replace with your actual COM port for the Arduino
    baudrate=9600,
    timeout=1
)


# Function to send a command and read the response from the titrator
def send_titrator_command(command):
    titrator_ser.write((command + '\r\n').encode())
    time.sleep(0.1)
    response = titrator_ser.read(titrator_ser.in_waiting).decode().strip()
    return response


# Function to send a command to the Arduino
def send_arduino_command(command):
    arduino_ser.write((command + '\r\n').encode())
    time.sleep(0.1)
    response = arduino_ser.read(arduino_ser.in_waiting).decode().strip()
    return response


# Initialize the titrator and prepare it for dosing
send_titrator_command('$L(dose_method)')  # Load the dosing method
send_titrator_command('$G')  # Start the method

# Prepare to log data
log_file = 'titrator_log.csv'
fields = ['Time', 'Acid Volume Dosed (ml)', 'Acid Concentration (M)', 'Sample Volume (ml)']
data = []

# Example parameters (these would be read from your experiment setup)
acid_concentration = 0.1  # Molarity of the acid
sample_volume = 50  # Volume of the sample in ml

try:
    while True:
        # Start the pump to dispense the sample
        send_arduino_command('S')
        print("Pump started to dispense sample")

        # Wait for a predefined time to dispense the sample (adjust as needed)
        time.sleep(10)  # Adjust this time based on your needs

        # Stop the pump
        send_arduino_command('P')
        print("Pump stopped after dispensing sample")

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

except KeyboardInterrupt:
    print("Terminating the titration process.")

finally:
    titrator_ser.close()
    arduino_ser.close()
