import serial
import time
import csv

# Setup the serial connection
ser = serial.Serial(
    port='COM2',  # Adjust the COM port as necessary
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)


# Function to send command to the titrator and read response
def send_command(command):
    ser.write((command + '\r\n').encode())
    response = ser.read_until(b'\r\n').decode().strip()
    return response


# Function to start dosing
def start_dosing():
    send_command('$G CR LF')  # Start command


# Function to stop dosing
def stop_dosing():
    send_command('$S')  # Stop command


# Function to check readiness
def check_ready():
    status = send_command('$D')
    return 'Ready' in status


# Function to get dosed volume
def get_dosed_volume():
    response = send_command('$Q(VOLUME)')
    if 'OK' in response:
        return response.split('=')[1]
    return None


# Main function to control dosing and record data
def control_dosing_and_record():
    output_file = 'dosed_volumes.csv'
    fieldnames = ['Timestamp', 'Dosed Volume (mL)']

    with open(output_file, 'w', newline='') as csvfile:
        csv_writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        csv_writer.writeheader()

        try:
            while True:
                if check_ready():
                    start_dosing()
                    time.sleep(1)  # Adjust the delay as necessary
                    stop_dosing()

                    volume = get_dosed_volume()
                    if volume:
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        csv_writer.writerow({'Timestamp': timestamp, 'Dosed Volume (mL)': volume})
                        print(f"{timestamp}: {volume} mL dosed")

                    time.sleep(10)  # Adjust the sampling rate as necessary

        except KeyboardInterrupt:
            print("Dosing stopped by user")


# Run the main function
if __name__ == "__main__":
    control_dosing_and_record()
