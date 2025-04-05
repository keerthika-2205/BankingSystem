import mysql.connector


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword",
    database="banking"
)
cursor = conn.cursor()



class Customer:
    def __init__(self, customer_id=None, first_name=None, last_name=None, email=None, phone=None, address=None):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone
        self.address = address

    def display_customer_info(self):
        print(
            f"Customer ID: {self.customer_id}\nFirst Name: {self.first_name}\nLast Name: {self.last_name}\nEmail: {self.email}\nPhone: {self.phone}\nAddress: {self.address}\n")



class Account:
    def __init__(self, account_id=None, account_type=None, balance=0.0):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = balance

    def save_to_db(self):

        cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s",
                       (self.balance, self.account_id))
        conn.commit()

    def deposit(self, amount):

        self.balance += amount
        self.save_to_db()
        print(f"Deposited {amount}. New Balance: {self.balance}")

    def withdraw(self, amount):

        if self.balance >= amount:
            self.balance -= amount
            self.save_to_db()
            print(f"Withdrawn {amount}. New Balance: {self.balance}")
        else:
            print("Insufficient balance!")

    def calculate_interest(self):

        if self.account_type.lower() == "savings":
            interest = self.balance * 0.045  # 4.5% interest
            self.balance += interest
            self.save_to_db()
            print(f"Interest added: {interest}. New Balance: {self.balance}")
        else:
            print("Interest calculation is only available for savings accounts.")

    def display_account_info(self):
        print(f"Account ID: {self.account_id}\nAccount Type: {self.account_type}\nBalance: {self.balance}\n")



class Bank:
    @staticmethod
    def create_account():
        """Creates a new bank account and stores it in the database."""
        acc_type = input("Enter Account Type (Savings/Current): ")
        balance = float(input("Enter Initial Balance: "))

        cursor.execute("INSERT INTO accounts (account_type, balance) VALUES (%s, %s)", (acc_type, balance))
        conn.commit()

        account_id = cursor.lastrowid  # Get the last inserted ID
        print(f"Account Created Successfully! Account ID: {account_id}")
        return Account(account_id, acc_type, balance)

    @staticmethod
    def perform_operations():

        account_id = input("Enter Account ID: ")


        cursor.execute("SELECT account_type, balance FROM accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()

        if result:
            acc_type, balance = result
            account = Account(account_id, acc_type, balance)

            while True:
                print("\nBanking System Menu:")
                print("1. Deposit\n2. Withdraw\n3. Calculate Interest\n4. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                elif choice == "2":
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)
                elif choice == "3":
                    account.calculate_interest()
                elif choice == "4":
                    print("Exiting...")
                    break
                else:
                    print("Invalid option! Please try again.")
        else:
            print("Account not found!")



if __name__ == "__main__":
    while True:
        print("\nBanking System Main Menu:")
        print("1. Create Account\n2. Perform Account Operations\n3. Exit")

        option = input("Enter your choice: ")

        if option == "1":
            Bank.create_account()
        elif option == "2":
            Bank.perform_operations()
        elif option == "3":
            print("Exiting System...")
            break
        else:
            print("Invalid Choice! Please enter 1, 2, or 3.")


cursor.close()
conn.close()
