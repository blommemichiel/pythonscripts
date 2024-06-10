import bluetooth
import argparse
import logging
import sys

# Set up logging
logging.basicConfig(filename='bluetooth_scan.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def scan_bluetooth_devices(duration):
    try:
        # Discover Bluetooth devices with names and classes.
        discovered_devices = bluetooth.discover_devices(duration=duration, lookup_names=True, lookup_class=True)
        
        # Display information about the scanning process.
        print('[!] Scanning for active devices...')
        print(f"[!] Found {len(discovered_devices)} Devices\n")
        logging.info(f"Found {len(discovered_devices)} devices.")

        # Iterate through discovered devices and print their details.
        for addr, name, device_class in discovered_devices:
            device_info = f'[+] Name: {name}\n[+] Address: {addr}\n[+] Device Class: {device_class}\n'
            print(device_info)
            logging.info(device_info)
    
    except bluetooth.BluetoothError as bt_error:
        error_message = f"[ERROR] Bluetooth error occurred: {bt_error}"
        print(error_message)
        logging.error(error_message)
    except Exception as e:
        error_message = f"[ERROR] An unexpected error occurred: {e}"
        print(error_message)
        logging.error(error_message)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Scan for Bluetooth devices.')
    parser.add_argument('-d', '--duration', type=int, default=8, 
                        help='Duration for scanning in seconds (default is 8 seconds)')
    
    args = parser.parse_args()
    
    # Call the Bluetooth device scanning function with the specified duration
    scan_bluetooth_devices(args.duration)

if __name__ == "__main__":
    main()
