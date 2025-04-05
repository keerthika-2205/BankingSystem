from abc import ABC, abstractmethod
import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword",
    database="banking"
)
cursor = conn.cursor()

class BankAccount(ABC):
    def __init__(self, account_number, customer_id, balance):
        self.account_number = account_number
        self.customer_id = customer_id
        self.balance = balance

    def get_account_number(self):
        return self.account_number

    def get_customer_id(self):
        return self.customer_id

    def get_balance(self):
        return self.balance

    def set_balance(self, new_balance):
        self.balance = new_balance

    def display_account_info(self):
        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()

        customer_name = cursor.fetchone()[0]
        print(f"\nAccount Number: {self.account_number}")
        print(f"Customer Name: {customer_name}")
        print(f"Balance: {self.balance}\n")


    def deposit(self, amount):
        pass
    def withdraw(self, amount):
        pass

    def calculate_interest(self):
        pass

class SavingsAccount(BankAccount):
    INTEREST_RATE = 0.045

    def __init__(self, account_number, customer_id, balance):
        super().__init__(account_number, customer_id, balance)

    def deposit(self, amount):
        self.balance += amount
        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()

        print(f"Deposited {amount}. New Balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            first_name = input("Enter Customer First Name: ")
            last_name = input("Enter Customer Last Name: ")
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

            cursor.execute(
                "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
                (first_name, last_name, dob)
            )
            conn.commit()

            print(f"Withdrawn {amount}. New Balance: {self.balance}")
        else:
            print("Insufficient balance!")

    def calculate_interest(self):
        interest = self.balance * SavingsAccount.INTEREST_RATE
        self.balance += interest
        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()

        print(f"Interest added: {interest}. New Balance: {self.balance}")

class CurrentAccount(BankAccount):
    OVERDRAFT_LIMIT = 5000

    def __init__(self, account_number, customer_id, balance):
        super().__init__(account_number, customer_id, balance)

    def deposit(self, amount):
        self.balance += amount
        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()

        print(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        if self.balance - amount >= -CurrentAccount.OVERDRAFT_LIMIT:
            self.balance -= amount
            first_name = input("Enter Customer First Name: ")
            last_name = input("Enter Customer Last Name: ")
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

            cursor.execute(
                "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
                (first_name, last_name, dob)
            )
            conn.commit()

            print(f"Withdrawn {amount}. New Balance: {self.balance}")
        else:
            print("Withdrawal denied! Overdraft limit exceeded.")

    def calculate_interest(self):
        print("No interest for Current Accounts.")

class Bank:

    def create_account():
        print("\nChoose Account Type:")
        print("1. Savings Account")
        print("2. Current Account")
        choice = input("Enter choice (1 or 2): ")

        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")
        balance = float(input("Enter Initial Balance: "))

        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()

        cursor.execute("SELECT LAST_INSERT_ID()")
        customer_id = cursor.fetchone()[0]

        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()


        acc_type = "Savings" if choice == "1" else "Current"

         first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")

        first_name = input("Enter Customer First Name: ")
        last_name = input("Enter Customer Last Name: ")
        dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

        cursor.execute(
            "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
            (first_name, last_name, dob)
        )
        conn.commit()

        print(f"Account created successfully! Your Account ID: {acc_num}")

        if choice == "1":
            return SavingsAccount(acc_num, customer_id, balance)
        else:
            return CurrentAccount(acc_num, customer_id, balance)


    def perform_operations(account):
        while True:
            print("\nBanking System Menu:")
            print("1. Deposit\n2. Withdraw\n3. Calculate Interest\n4. Exit")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
            elif choice == 2:
                amount = float(input("Enter amount to withdraw: "))
                account.withdraw(amount)
            elif choice == 3:
                account.calculate_interest()
            elif choice == 4:
                print("Exiting...")
                break
            else:
                print("Invalid option!")

if __name__ == "__main__":
    while True:
        print("\nBanking System Main Menu:")
        print("1. Create Account\n2. Perform Account Operations\n3. Exit")
        option = int(input("Enter your choice: "))

        if option == 1:
            account = Bank.create_account()
            if account:
                print("Account Created Successfully!")
                account.display_account_info()
        elif option == 2:
            acc_num = input("Enter Account Number: ")
            first_name = input("Enter Customer First Name: ")
            last_name = input("Enter Customer Last Name: ")
            dob = input("Enter Date of Birth (YYYY-MM-DD): ")  # Format matters!

            cursor.execute(
                "INSERT INTO customers (first_name, last_name, DOB) VALUES (%s, %s, %s)",
                (first_name, last_name, dob)
            )
            conn.commit()

            result = cursor.fetchone()

            if result:
                customer_id, acc_type, balance = result
                if acc_type == "Savings":
                    account = SavingsAccount(acc_num, customer_id, balance)
                else:
                    account = CurrentAccount(acc_num, customer_id, balance)

                Bank.perform_operations(account)
            else:
                print("Account not found!")

        elif option == 3:
            print("Exiting System...")
            break
        else:
            print("Invalid Choice!")

cursor.close()
conn.close()
