# Banking System

A Python-based banking system that allows users to manage their accounts, perform transactions, and access essential banking features. This project is designed to simulate basic banking operations and is perfect for educational purposes.

## Features

1. **User Account Management**:
  - Create accounts with different types (Savings, Current, Salary).
  - Unique account numbers and usernames are auto-generated.

2. **Authentication:**
   - Secure login system using hashed passwords.
   - 4-digit PIN verification for sensitive operations.

3. **Transaction Features**:
  - Check account balance with warnings for low balances.
  - Deposit and withdraw money.
  - Transfer money to other accounts.
  - View and generate transaction statements.

4. **Currency Management**:
  - Change account currency (Supported: USD, EUR, INR, GBP).
  Currency conversion with real-time updates.

5. **Loan Management**:
  - Apply for loans with fixed interest rates.
  - EMI calculation and next due date tracking.

6. **Additional Features:**
   - Account deletion.
   - Transaction logging for auditing.
   - Warnings for low balance.

## Prerequisites

- Python 3.8 or higher

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/yourusername/BankingSystem.git
   ```

2. Navigate to the project directory:
   ```bash
   cd BankingSystem
   ```

3. Install required libraries:
   ```bash
   pip install colorama
   ```

4. Ensure you have the required files:
   - `SourceCode.py` (Main script)
   - `users.json` (For storing user data)
   - `transactions.json` (For storing transaction data)
   - `currencies.json` (For storing currency data)
   - `loans.json` (For storing loan data)
   - `config.json` (For storing configuration data)

## Usage

- Follow the menu options in the console to use the banking system.
- Perform operations like creating an account, depositing money, applying for loans, and more.

## How to Run

1. Open a terminal in the project directory.
2. Run the following command:
   ```bash
   python SourceCode.py
   ```
3. Follow the on-screen instructions to create accounts, perform transactions, and explore other features.

## Notes

- Passwords are securely stored using SHA-256 hashing.
- Currency conversion rates are hardcoded for simulation purposes and may not reflect real-world rates.
- Ensure that the `users.json` and `transactions.json` files have proper read/write permissions.

## Future Enhancements

- Add a graphical user interface (GUI).
- Implement real-time exchange rate updates.
- Add more detailed loan management features.
- Add MultiFactor Verification. 
- Add more detailed transaction history.
- Add more detailed user profile management.

## Contributions

Contributions to improve the project are welcome! Feel free to fork the repository and submit pull requests.

## License

This project is for educational purposes and is open-source. Feel free to contribute or modify as needed!

---

Enjoy using the Banking System. 😊
