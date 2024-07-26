import serial

# Configure the serial connection
ser = serial.Serial(
    port='COM3',  # Replace with your COM port
    baudrate=9600,  # Adjust to match device settings
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def send_command(command):
    ser.write(command.encode())
    response = ser.read(100)  # Adjust buffer size as needed
    return response.decode()

# Example command to the Dosimat
command = 'YOUR_COMMAND_HERE'
response = send_command(command)
print(f"Response: {response}")

ser.close()
