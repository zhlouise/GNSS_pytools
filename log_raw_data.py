import serial
import threading
import datetime
from pyubx2 import UBXReader

def log_gnss_data(port, name, log_directory="."):
    """Reads UBX messages and logs them to a file."""
    try:
        ser = serial.Serial(port, baudrate=115200, timeout=1)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_filename = f"{log_directory}/{name}_{timestamp}.ubx"
        ubx_reader = UBXReader(ser)

        with open(log_filename, "wb") as log_file:
            print(f"[{name}] Starting to log raw data to {log_filename}...")

            # UBXReader automatically detects and parses UBX messages
            for raw_data, parsed_data in ubx_reader:
                if raw_data:
                    log_file.write(raw_data)

    except serial.SerialException as e:
        print(f"Error reading from {name}: {e}")
    except Exception as e:
        print(f"An unexpected error occurred for {name}: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
        print(f"[{name}] Stopping data collection.")

if __name__ == "__main__":
    # Change these to match your identified serial ports
    port1 = '/dev/ttyACM0'
    port2 = '/dev/ttyACM1'

    # Give your receivers descriptive names
    thread1 = threading.Thread(target=log_gnss_data, args=(port1, "Upper"))
    thread2 = threading.Thread(target=log_gnss_data, args=(port2, "Lower"))

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()
