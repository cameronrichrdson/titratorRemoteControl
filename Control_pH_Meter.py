import serial
import time
import csv

ser = serial.Serial(
    port='COM2',  # Adjust the COM port as necessary
    baudrate=9600,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    timeout=1
)

    def send_command(self, command):
        """Send a command to the meter."""
        if not command.endswith("\r"):
            command += "\r"
        self.ser.write(command.encode())
        time.sleep(0.5)  # Ensure the meter has enough time to process
        return self.read_response()


    def get_log(self, start=None, end=None):
        """Get logged measurement data."""
        command = "GETLOG"
        if start and end:
            command += f" {start} {end}"
        return self.send_command(command)

    def get_system_info(self):
        """Get system information."""
        return self.send_command("SYSTEM")

    def set_date_time(self, yy, mm, dd, hh, mi, ss):
        """Set the date and time on the meter."""
        command = f"SETRTC {yy:02} {mm:02} {dd:02} {hh:02} {mi:02} {ss:02}"
        return self.send_command(command)

    def set_mode(self, mode):
        """Set the current channel measurement mode."""
        command = f"SETMODE {mode}"
        return self.send_command(command)

    def get_mode(self, channel):
        """Get the measurement mode of a specific channel."""
        command = f"GETMODE {channel}"
        return self.send_command(command)

    def set_csv_format(self):
        """Set the printing format to CSV."""
        return self.send_command("SETCSV")

    def set_key_lock(self, lock):
        """Enable or disable the keypad."""
        command = f"SETKEYLOCK {int(lock)}"
        return self.send_command(command)

    def close(self):
        """Close the serial connection."""
        self.ser.close()

# Example usage:
# meter = StarA200A300Meter(port='/dev/ttyUSB0')
# print(meter.get_measurement())
# meter.close()
