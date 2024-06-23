import subprocess
import os
import re
from collections import namedtuple
import configparser


class WifiProfileExtractor:
    def __init__(self, verbose=1):
        self.verbose = verbose
        self.Profile = namedtuple("Profile", ["ssid", "ciphers", "key"])
        
    def print_profile(self, profile):
        if os.name == 'nt':
            print(f"{profile.ssid:25}{profile.ciphers:15}{profile.key:50}")
        elif os.name == 'posix':
            print(f"{str(profile.ssid):25}{str(profile.auth_alg):5}{str(profile.key_mgmt):10}{str(profile.psk):50}")

    def print_headers(self):
        if os.name == 'nt':
            print("SSID                     CIPHER(S)      KEY")
        elif os.name == 'posix':
            print("SSID                     AUTH KEY-MGMT  PSK")
        print("-"*50)
        
    def get_windows_saved_ssids(self):
        try:
            output = subprocess.check_output("netsh wlan show profiles").decode()
            profiles = re.findall(r"All User Profile\s*:\s*(.*)", output)
            ssids = [profile.strip() for profile in profiles]
            return ssids
        except subprocess.CalledProcessError as e:
            print(f"Error retrieving SSIDs: {e}")
            return []

    def get_windows_saved_wifi_passwords(self):
        ssids = self.get_windows_saved_ssids()
        profiles = []
        for ssid in ssids:
            try:
                ssid_details = subprocess.check_output(f"netsh wlan show profile \"{ssid}\" key=clear").decode()
                ciphers = re.findall(r"Cipher\s*:\s*(.*)", ssid_details)
                ciphers = "/".join([c.strip() for c in ciphers])
                key = re.findall(r"Key Content\s*:\s*(.*)", ssid_details)
                key = key[0].strip() if key else "None"
                profile = self.Profile(ssid=ssid, ciphers=ciphers, key=key)
                if self.verbose >= 1:
                    self.print_profile(profile)
                profiles.append(profile)
            except subprocess.CalledProcessError as e:
                print(f"Error retrieving details for SSID {ssid}: {e}")
        return profiles

    def get_linux_saved_wifi_passwords(self):
        network_connections_path = "/etc/NetworkManager/system-connections/"
        fields = ["ssid", "auth-alg", "key-mgmt", "psk"]
        Profile = namedtuple("Profile", [f.replace("-", "_") for f in fields])
        profiles = []
        
        try:
            for file in os.listdir(network_connections_path):
                data = {k.replace("-", "_"): None for k in fields}
                config = configparser.ConfigParser()
                config.read(os.path.join(network_connections_path, file))
                for section in config.sections():
                    for k, v in config.items(section):
                        if k in fields:
                            data[k.replace("-", "_")] = v
                profile = Profile(**data)
                if self.verbose >= 1:
                    self.print_profile(profile)
                profiles.append(profile)
        except Exception as e:
            print(f"Error retrieving Linux Wi-Fi profiles: {e}")
        return profiles

    def extract_profiles(self):
        self.print_headers()
        if os.name == 'nt':
            return self.get_windows_saved_wifi_passwords()
        elif os.name == 'posix':
            return self.get_linux_saved_wifi_passwords()
        else:
            raise NotImplementedError("This code only works for Linux or Windows operating systems")


if __name__ == "__main__":
    extractor = WifiProfileExtractor(verbose=1)
    extractor.extract_profiles()
