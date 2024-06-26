import subprocess, platform, re
from colorama import init, Fore


init()

def list_open_networks():
    # Get the name of the operating system.
    os_name = platform.system()

    if os_name == "Windows":
        # Command to list Wi-Fi networks on Windows.
        list_networks_command = 'netsh wlan show networks'
        try:
            # Execute the command and capture the output.
            output = subprocess.check_output(list_networks_command, shell=True, text=True)
            networks = []

            ssid = None
            # Parse the output to find open Wi-Fi networks.
            for line in output.splitlines():
                if "SSID" in line:
                    # Extract the SSID (Wi-Fi network name).
                    ssid = line.split(":")[1].strip()
                elif "Authentication" in line and "Open" in line and ssid:
                    # Check if the Wi-Fi network has open authentication.
                    networks.append(ssid)
                    ssid = None

            # Print the list of open networks
            print_open_networks(networks)

        except subprocess.CalledProcessError as e:
            # Handle any errors that occur during the execution of the command.
            print(f"{Fore.RED}Error executing command: {e}")
        except Exception as e:
            # Handle any other exceptions.
            print(f"{Fore.RED}An error occurred: {e}")

    elif os_name == "Linux":
        try:
            # Run nmcli to list available Wi-Fi networks.
            result = subprocess.run(["nmcli", "--terse", "--fields", "SECURITY,SSID", "device", "wifi", "list"],
                                    stdout=subprocess.PIPE, text=True, check=True)
            # Access the captured stdout.
            output = result.stdout.strip()
            networks = []

            # Parse the output to find open Wi-Fi networks.
            for line in output.splitlines():
                # Split the line into security and SSID fields.
                security, ssid = line.split(':')
                # Check if the network is open (no security).
                if security == "--":
                    networks.append(ssid)

            # Print the list of open networks
            print_open_networks(networks)

        except subprocess.CalledProcessError as e:
            # Handle errors running nmcli.
            print(f"{Fore.RED}Error running nmcli: {e}")
        except Exception as e:
            # Handle any other exceptions.
            print(f"{Fore.RED}An error occurred: {e}")

    else:
        # Inform the user if the operating system is not supported.
        print(f"{Fore.RED}Unsupported operating system.")

def print_open_networks(networks):
    # Check if any open networks were found.
    if networks:
        # Print a message for open networks with colored output.
        print(f'{Fore.LIGHTMAGENTA_EX}[+] Open Wi-Fi networks in range:\n')
        for each_network in networks:
            print(f"{Fore.GREEN}[+] {each_network}")
    else:
        # Print a message if no open networks were found.
        print(f"{Fore.RED}[-] No open Wi-Fi networks in range.")

# Call the function to list open networks.
if __name__ == "__main__":
    list_open_networks()

