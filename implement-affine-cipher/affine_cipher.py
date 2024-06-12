import string
from colorama import init, Fore
from math import gcd

# Initialize colorama.
init()

# Function to check if 'a' is coprime with m (length of the alphabet)
def is_coprime(a, m):
    return gcd(a, m) == 1

# Function to perform Affine Cipher encryption.
def affine_encryption(plaintext, a, b):
    # Define the alphabets.
    uppercase_alphabet = string.ascii_uppercase
    lowercase_alphabet = string.ascii_lowercase
    # Get the length of the alphabet
    m = len(uppercase_alphabet)
    # Initialize an empty string to store the ciphertext.
    ciphertext = ''

    # Iterate through each character in the plaintext.
    for char in plaintext:
        if char in uppercase_alphabet:
            # Encrypt uppercase characters.
            p = uppercase_alphabet.index(char)
            c = (a * p + b) % m
            ciphertext += uppercase_alphabet[c]
        elif char in lowercase_alphabet:
            # Encrypt lowercase characters.
            p = lowercase_alphabet.index(char)
            c = (a * p + b) % m
            ciphertext += lowercase_alphabet[c]
        else:
            # If the character is not in the alphabet, keep it unchanged.
            ciphertext += char

    # Return the encrypted ciphertext.
    return ciphertext

# Define the main function to run the encryption process.
def main():
    # Get user input for the plaintext.
    plaintext = input(f"{Fore.GREEN}[?] Enter text to encrypt: ")
    
    # Get user input for 'a' and 'b' with validation.
    while True:
        try:
            a = int(input(f"{Fore.GREEN}[?] Enter key 'a' (must be coprime with 26): "))
            if not is_coprime(a, 26):
                print(f"{Fore.RED}[!] 'a' must be coprime with 26. Please try again.")
                continue
            b = int(input(f"{Fore.GREEN}[?] Enter key 'b': "))
            break
        except ValueError:
            print(f"{Fore.RED}[!] Invalid input. Please enter integers for 'a' and 'b'.")

    # Call the affine_encryption function with the specified parameters.
    encrypted_text = affine_encryption(plaintext, a, b)

    # Print the original plaintext, the key components, and the encrypted text.
    print(f"{Fore.MAGENTA}[+] Plaintext: {plaintext}")
    print(f"{Fore.CYAN}[+] Key 'a': {a}, Key 'b': {b}")
    print(f"{Fore.GREEN}[+] Encrypted Text: {encrypted_text}")

# Run the main function.
if __name__ == "__main__":
    main()
