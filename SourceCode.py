import os
import hashlib
import json
from datetime import datetime, timedelta
import random
from colorama import Fore, Style

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_data(filename, data):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as file:
            return json.load(file)
    return {}

def generate_account_number():
    return str(random.randint(1000000000, 9999999999))

def is_non_continuous_pin(pin):
    continuous_sequences = ["1234", "2345", "3456", "4567", "5678", "6789", "7890", "0987", "9876", "8765", "7654", "6543", "5432", "4321", "1470", "2580"]
    return pin not in continuous_sequences

def get_exchange_rate(currency):
    # Mocked exchange rates relative to USD
    exchange_rates = {
        'USD': 1.0,
        'EUR': 0.85,
        'INR': 74.0,
        'GBP': 0.75
    }
    return exchange_rates.get(currency, 1.0)

def calculate_emi(principal, rate, tenure_months):
    monthly_rate = rate / (12 * 100)
    emi = principal * monthly_rate * (1 + monthly_rate) ** tenure_months / ((1 + monthly_rate) ** tenure_months - 1)
    return round(emi, 2)

class BankingSystem:
    def __init__(self):
        self.users_file = 'users.json'
        self.transactions_file = 'transactions.json'
        self.transaction_log_file = 'transaction_log.txt'
        self.users = load_data(self.users_file)
        self.transactions = load_data(self.transactions_file)

    def create_account(self):
        print(Fore.CYAN + "Select Account Type:")
        print(Fore.GREEN + "1. Savings Account\n2. Current Account\n3. Salary Account" + Style.RESET_ALL)
        account_type = input(Fore.YELLOW + "Enter your choice: " + Style.RESET_ALL)
        if account_type not in ['1', '2', '3']:
            print(Fore.RED + "Invalid choice." + Style.RESET_ALL)
            return

        first_name = input(Fore.YELLOW + "Enter your first name: " + Style.RESET_ALL)
        last_name = input(Fore.YELLOW + "Enter your last name: " + Style.RESET_ALL)
        dob = input(Fore.YELLOW + "Enter your date of birth (YYYY-MM-DD): " + Style.RESET_ALL)
        gender = input(Fore.YELLOW + "Enter your gender: " + Style.RESET_ALL)

        username = f"{first_name[:3]}{last_name[:3]}{random.randint(100, 999)}"
        print(Fore.GREEN + f"Your generated username is: {username}" + Style.RESET_ALL)

        password = input(Fore.YELLOW + "Create your password: " + Style.RESET_ALL)
        if not (any(c.isupper() for c in password) and any(c.islower() for c in password) and any(c.isdigit() for c in password) and any(c in '!@#$%^&*' for c in password)):
            print(Fore.RED + "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character." + Style.RESET_ALL)
            return

        pin = input(Fore.YELLOW + "Set a unique 4-digit PIN: " + Style.RESET_ALL)
        if len(pin) != 4 or not pin.isdigit() or not is_non_continuous_pin(pin):
            print(Fore.RED + "PIN must be a 4-digit number and cannot be continuous sequences like '1234' or '2580'." + Style.RESET_ALL)
            return

        account_number = generate_account_number()
        self.users[username] = {
            'password': hash_password(password),
            'account_number': account_number,
            'pin': pin,
            'balance': 0.0,
            'currency': 'INR',
            'account_type': account_type,
            'first_name': first_name,
            'last_name': last_name,
            'dob': dob,
            'gender': gender,
            'transactions': [],
            'loan': None
        }
        save_data(self.users_file, self.users)
        print(Fore.GREEN + f"Account created successfully! Your account number is {account_number}." + Style.RESET_ALL)

    def login(self):
        account_number = input(Fore.YELLOW + "Enter account number: " + Style.RESET_ALL)
        password = input(Fore.YELLOW + "Enter password: " + Style.RESET_ALL)
        user = next((user for user, data in self.users.items() if data['account_number'] == account_number), None)
        if user and self.users[user]['password'] == hash_password(password):
            print(Fore.GREEN + "Login successful!" + Style.RESET_ALL)
            self.user_menu(user)
        else:
            print(Fore.RED + "Invalid credentials." + Style.RESET_ALL)

    def user_menu(self, username):
        while True:
            print(Fore.CYAN + "\n1. Check Balance\n2. Deposit\n3. Withdraw\n4. Transfer\n5. View Transactions\n6. Generate Statement\n7. Delete Account\n8. Change Currency\n9. Apply for Loan\n10. Logout" + Style.RESET_ALL)
            choice = input(Fore.YELLOW + "Choose an option: " + Style.RESET_ALL)
            if choice == '1':
                self.check_balance(username)
            elif choice == '2':
                self.deposit(username)
            elif choice == '3':
                self.withdraw(username)
            elif choice == '4':
                self.transfer(username)
            elif choice == '5':
                self.view_transactions(username)
            elif choice == '6':
                self.generate_statement(username)
            elif choice == '7':
                self.delete_account(username)
                break
            elif choice == '8':
                self.change_currency(username)
            elif choice == '9':
                self.apply_for_loan(username)
            elif choice == '10':
                print(Fore.GREEN + "Logged out successfully." + Style.RESET_ALL)
                break
            else:
                print(Fore.RED + "Invalid choice." + Style.RESET_ALL)

    def check_balance(self, username):
        pin = input(Fore.YELLOW + "Enter your 4-digit PIN: " + Style.RESET_ALL)
        if pin == self.users[username]['pin']:
            currency = self.users[username]['currency']
            balance = self.users[username]['balance']
            print(Fore.GREEN + f"Your balance is: {balance:.2f} {currency}" + Style.RESET_ALL)
            if balance < 50:
                print(Fore.RED + "Warning: Your balance is low." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid PIN." + Style.RESET_ALL)

    def deposit(self, username):
        amount = float(input(Fore.YELLOW + "Enter amount to deposit: " + Style.RESET_ALL))
        if amount > 0:
            self.users[username]['balance'] += amount
            self.log_transaction(username, f"Deposited {amount:.2f} {self.users[username]['currency']}")
            print(Fore.GREEN + "Deposit successful." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid amount." + Style.RESET_ALL)

    def withdraw(self, username):
        pin = input(Fore.YELLOW + "Enter your 4-digit PIN: " + Style.RESET_ALL)
        if pin == self.users[username]['pin']:
            amount = float(input(Fore.YELLOW + "Enter amount to withdraw: " + Style.RESET_ALL))
            if 0 < amount <= self.users[username]['balance']:
                self.users[username]['balance'] -= amount
                self.log_transaction(username, f"Withdrew {amount:.2f} {self.users[username]['currency']}")
                print(Fore.GREEN + "Withdrawal successful." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Insufficient balance or invalid amount." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid PIN." + Style.RESET_ALL)

    def transfer(self, username):
        recipient_account = input(Fore.YELLOW + "Enter recipient account number: " + Style.RESET_ALL)
        recipient = next((user for user, data in self.users.items() if data['account_number'] == recipient_account), None)
        if not recipient:
            print(Fore.RED + "Recipient account does not exist." + Style.RESET_ALL)
            return
        pin = input(Fore.YELLOW + "Enter your 4-digit PIN: " + Style.RESET_ALL)
        if pin == self.users[username]['pin']:
            amount = float(input(Fore.YELLOW + "Enter amount to transfer: " + Style.RESET_ALL))
            if 0 < amount <= self.users[username]['balance']:
                self.users[username]['balance'] -= amount
                self.users[recipient]['balance'] += amount
                self.log_transaction(username, f"Transferred {amount:.2f} {self.users[username]['currency']} to account {recipient_account}")
                self.log_transaction(recipient, f"Received {amount:.2f} {self.users[username]['currency']} from account {self.users[username]['account_number']}")
                print(Fore.GREEN + "Transfer successful." + Style.RESET_ALL)
            else:
                print(Fore.RED + "Insufficient balance or invalid amount." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid PIN." + Style.RESET_ALL)

    def view_transactions(self, username):
        transactions = self.users[username]['transactions']
        if not transactions:
            print(Fore.RED + "No transactions found." + Style.RESET_ALL)
        else:
            for transaction in transactions:
                print(transaction)

    def generate_statement(self, username):
        month = input(Fore.YELLOW + "Enter the month (MM) for the statement: " + Style.RESET_ALL)
        year = input(Fore.YELLOW + "Enter the year (YYYY) for the statement: " + Style.RESET_ALL)
        transactions = self.users[username]['transactions']
        statement = [t for t in transactions if t.startswith(f"{year}-{month}")]
        if not statement:
            print(Fore.RED + "No transactions found for the specified period." + Style.RESET_ALL)
        else:
            print(Fore.CYAN + "Statement:" + Style.RESET_ALL)
            for transaction in statement:
                print(transaction)

    def delete_account(self, username):
        confirm = input(Fore.YELLOW + "Are you sure you want to delete your account? (yes/no): " + Style.RESET_ALL).lower()
        if confirm == 'yes':
            del self.users[username]
            save_data(self.users_file, self.users)
            print(Fore.GREEN + "Account deleted successfully." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Account deletion canceled." + Style.RESET_ALL)

    def log_transaction(self, username, transaction):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {transaction}\n"
        self.users[username]['transactions'].append(log_entry)
        save_data(self.users_file, self.users)
        with open(self.transaction_log_file, 'a') as file:
            file.write(log_entry)

    def change_currency(self, username):
        print(Fore.CYAN + "Available currencies: USD, EUR, INR, GBP" + Style.RESET_ALL)
        new_currency = input(Fore.YELLOW + "Enter new currency: " + Style.RESET_ALL)
        if new_currency in ['USD', 'EUR', 'INR', 'GBP']:
            exchange_rate = get_exchange_rate(new_currency) / get_exchange_rate(self.users[username]['currency'])
            self.users[username]['balance'] *= exchange_rate
            self.users[username]['currency'] = new_currency
            save_data(self.users_file, self.users)
            print(Fore.GREEN + f"Currency changed to {new_currency}." + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid currency." + Style.RESET_ALL)

    def apply_for_loan(self, username):
        principal = float(input(Fore.YELLOW + "Enter loan amount: " + Style.RESET_ALL))
        tenure_years = int(input(Fore.YELLOW + "Enter loan tenure in years: " + Style.RESET_ALL))
        tenure_months = tenure_years * 12
        rate = 15  # Interest rate in percent
        emi = calculate_emi(principal, rate, tenure_months)
        self.users[username]['loan'] = {
            'principal': principal,
            'tenure_months': tenure_months,
            'rate': rate,
            'emi': emi,
            'next_due_date': (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
        }
        save_data(self.users_file, self.users)
        print(Fore.GREEN + f"Loan approved! Your EMI is {emi:.2f} per month." + Style.RESET_ALL)

if __name__ == "__main__":
    banking_system = BankingSystem()
    while True:
        print(Fore.CYAN + "\nWelcome to the Banking System" + Style.RESET_ALL)
        print(Fore.GREEN + "1. Create Account\n2. Login\n3. Exit" + Style.RESET_ALL)
        choice = input(Fore.YELLOW + "Choose an option: " + Style.RESET_ALL)
        if choice == '1':
            banking_system.create_account()
        elif choice == '2':
            banking_system.login()
        elif choice == '3':
            print(Fore.GREEN + "Thank you for using the Banking System. Goodbye!" + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again." + Style.RESET_ALL)
