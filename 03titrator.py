import serial
import time
import csv

# Set up the serial connection (adjust COM port as needed)
ser = serial.Serial(
    port='COM1',  # Replace with your actual COM port
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    stopbits=serial.STOPBITS_ONE,
    parity=serial.PARITY_NONE,
    timeout=1
)


# Function to send a command and read the response
def send_command(command):
    ser.write((command + '\r\n').encode())
    time.sleep(0.1)
    response = ser.read(ser.in_waiting).decode().strip()
    return response


# Initialize the titrator and prepare it for dosing
send_command('$L(dose_method)')  # Load the dosing method
send_command('$G')  # Start the method

# Prepare to log data
log_file = 'titrator_log.csv'
fields = ['Time', 'Acid Volume Dosed (ml)', 'Acid Concentration (M)', 'Sample Volume (ml)']
data = []

# Example parameters (these would be read from your experiment setup)
acid_concentration = 0.1  # Molarity of the acid
sample_volume = 50  # Volume of the sample in ml

try:
    while True:
        # Trigger a dosing step
        send_command('$G')

        # Get the dosed volume
        dosed_volume = send_command('$Q(VOLUME)')

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
        time.sleep(1)

except KeyboardInterrupt:
    print("Terminating the titration process.")

finally:
    ser.close()
