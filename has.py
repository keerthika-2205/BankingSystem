import mysql.connector
import re

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword",
    database="banking"
)
cursor = conn.cursor()

class Customer:
    def __init__(self, first_name, last_name, email, phone_number, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.address = address

    def is_valid_email(self):
        return re.match(r"[^@]+@[^@]+\.[^@]+", self.email)

    def is_valid_phone(self):
        return re.match(r"^\d{10}$", self.phone_number)

class Account:
    def __init__(self, account_type, balance, customer_id):
        self.account_type = account_type
        self.balance = balance
        self.customer_id = customer_id

class Bank:
    def create_account(self):
        print("\n--- Enter Customer Information ---")
        first_name = input("First Name: ")
        last_name = input("Last Name: ")
        email = input("Email: ")
        phone = input("Phone (10 digits): ")
        address = input("Address: ")

        customer = Customer(first_name, last_name, email, phone, address)

        if not customer.is_valid_email() or not customer.is_valid_phone():
            print("Invalid email or phone number format.")
            return

        cursor.execute("""
            INSERT INTO customers (first_name, last_name, email, phone_number, address)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, address))
        conn.commit()
        customer_id = cursor.lastrowid

        print("\n--- Enter Account Details ---")
        acc_type = input("Account Type (Savings/Current): ")
        balance = float(input("Initial Balance: "))

        cursor.execute("""
            INSERT INTO accounts (account_type, balance, customer_id)
            VALUES (%s, %s, %s)
        """, (acc_type, balance, customer_id))
        conn.commit()

        print(" Account successfully created!\n")

    def get_account_balance(self, acc_id):
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (acc_id,))
        result = cursor.fetchone()
        if result:
            print(f"Current Balance: ₹{result[0]}")
        else:
            print(" Account not found.")

    def deposit(self, acc_id, amount):
        cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_id = %s", (amount, acc_id))
        conn.commit()
        self.get_account_balance(acc_id)

    def withdraw(self, acc_id, amount):
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (acc_id,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            cursor.execute("UPDATE accounts SET balance = balance - %s WHERE account_id = %s", (amount, acc_id))
            conn.commit()
            self.get_account_balance(acc_id)
        else:
            print(" Insufficient funds or account not found.")

    def transfer(self, from_acc, to_acc, amount):
        cursor.execute("SELECT balance FROM accounts WHERE account_id = %s", (from_acc,))
        result = cursor.fetchone()
        if result and result[0] >= amount:
            self.withdraw(from_acc, amount)
            self.deposit(to_acc, amount)
            print("Transfer successful.")
        else:
            print("Transfer failed. Check balance or account number.")

    def get_account_details(self, acc_id):
        cursor.execute("""
            SELECT a.account_id, a.account_type, a.balance,
                   c.first_name, c.last_name, c.email, c.phone_number, c.address
            FROM accounts a
            JOIN customers c ON a.customer_id = c.customer_id
            WHERE a.account_id = %s
        """, (acc_id,))
        result = cursor.fetchone()
        if result:
            print(f"""
Account Number: {result[0]}
Account Type: {result[1]}
Balance: ₹{result[2]}
Customer Name: {result[3]} {result[4]}
Email: {result[5]}
Phone: {result[6]}
Address: {result[7]}
""")
        else:
            print(" Account not found.")

def main():
    bank = Bank()
    while True:
        print("""
=== Banking System ===
1. Create Account
2. Deposit
3. Withdraw
4. Get Balance
5. Transfer
6. Get Account Details
7. Exit
        """)
        choice = input("Enter choice: ")

        if choice == '1':
            bank.create_account()
        elif choice == '2':
            acc = int(input("Enter Account Number: "))
            amt = float(input("Enter amount to deposit: "))
            bank.deposit(acc, amt)
        elif choice == '3':
            acc = int(input("Enter Account Number: "))
            amt = float(input("Enter amount to withdraw: "))
            bank.withdraw(acc, amt)
        elif choice == '4':
            acc = int(input("Enter Account Number: "))
            bank.get_account_balance(acc)
        elif choice == '5':
            from_acc = int(input("From Account Number: "))
            to_acc = int(input("To Account Number: "))
            amt = float(input("Amount to transfer: "))
            bank.transfer(from_acc, to_acc, amt)
        elif choice == '6':
            acc = int(input("Enter Account Number: "))
            bank.get_account_details(acc)
        elif choice == '7':
            print("Exiting")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
