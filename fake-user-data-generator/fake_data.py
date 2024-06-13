from faker import Faker
from faker.providers import internet
import csv


# Function to generate user data with the specified number of users.
def generate_user_data(num_of_users):
    fake = Faker()
    fake.add_provider(internet)
    user_data = []

    for _ in range(num_of_users):
        user = {
            'Name': fake.name(),
            'Email': fake.free_email(),
            'Phone Number': fake.phone_number(),
            'Birthdate': fake.date_of_birth(),
            'Address': fake.address(),
            'City': fake.city(),
            'Country': fake.country(),
            'ZIP Code': fake.zipcode(),
            'Job Title': fake.job(),
            'Company': fake.company(),
            'IP Address': fake.ipv4_private(),
            'Credit Card Number': fake.credit_card_number(),
            'Username': fake.user_name(),
            'Website': fake.url(),
            'SSN': fake.ssn()
        }
        user_data.append(user)

    return user_data


# Function to save user data to a CSV file.
def save_to_csv(data, filename):
    keys = data[0].keys()
    try:
        with open(filename, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=keys)
            writer.writeheader()
            for user in data:
                writer.writerow(user)
        print(f'[+] Data saved to {filename} successfully.')
    except IOError as e:
        print(f"[-] Failed to save data to {filename}. Error: {e}")


# Function to save user data to a text file.
def save_to_text(data, filename):
    try:
        with open(filename, 'w') as output_file:
            for user in data:
                for key, value in user.items():
                    output_file.write(f"{key}: {value}\n")
                output_file.write('\n')
        print(f'[+] Data saved to {filename} successfully.')
    except IOError as e:
        print(f"[-] Failed to save data to {filename}. Error: {e}")


# Function to print user data vertically.
def print_data_vertically(data):
    for user in data:
        for key, value in user.items():
            print(f"{key}: {value}")
        print()


def main():
    try:
        number_of_users = int(input("[!] Enter the number of users to generate: "))
    except ValueError:
        print("[-] Invalid input. Please enter a valid number.")
        return

    user_data = generate_user_data(number_of_users)
    
    save_option = input("[?] Do you want to save the data to a file? (yes/no): ").lower()
    
    if save_option == 'yes':
        file_type = input("[!] Enter file type (csv/txt/both): ").lower()
        if file_type in ['csv', 'both']:
            custom_filename_csv = input("[!] Enter the CSV filename (without extension): ")
            filename_csv = f"{custom_filename_csv}.csv"
            save_to_csv(user_data, filename_csv)
        
        if file_type in ['txt', 'both']:
            custom_filename_txt = input("[!] Enter the TXT filename (without extension): ")
            filename_txt = f"{custom_filename_txt}.txt"
            save_to_text(user_data, filename_txt)

        if file_type not in ['csv', 'txt', 'both']:
            print("[-] Invalid file type. Data not saved.")
    else:
        print_data_vertically(user_data)


if __name__ == "__main__":
    main()
