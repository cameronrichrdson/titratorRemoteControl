import serial
import time
import csv


def setup_serial_connection(port='COM2', baudrate=19200):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=1
        )
        print(f"Serial port {port} opened successfully.")
        return ser
    except serial.SerialException as e:
        print(f"Error opening serial port {port}: {e}")
        return None


def send_command(ser, command):
    if ser is None:
        print("Serial connection not established.")
        return None

    try:
        ser.write((command + '\r\n').encode())
        response = ser.read_until(b'\r\n').decode().strip()
        return response
    except serial.SerialException as e:
        print(f"Error sending command: {e}")
        return None


def start_dosing(ser):
    response = send_command(ser, '$G')  # Start command
    if response:
        print(f"Response: {response}")


# Setup the serial connection
#ser = setup_serial_connection()

# Start dosing
#start_dosing(ser)
