import mysql.connector
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword",
    database="banking"
)
cursor = conn.cursor()

class Account:
    def __init__(self, account_id, account_type, balance=0.0):
        self.account_id = account_id
        self.account_type = account_type
        self.balance = float(balance)  # Ensuring balance is a float

    def save_to_db(self):

        cursor.execute("UPDATE accounts SET balance = %s WHERE account_id = %s", (self.balance, self.account_id))
        conn.commit()

    def deposit(self, amount):
        if isinstance(amount, (int, float)):
            self.balance += float(amount)
            self.save_to_db()
            print(f"Deposited {amount}. New Balance: {self.balance}")
        else:
            print("Invalid amount. Please enter a number.")

    def withdraw(self, amount):
        if isinstance(amount, (int, float)):
            if self.balance >= float(amount):
                self.balance -= float(amount)
                self.save_to_db()
                print(f"Withdrawn {amount}. New Balance: {self.balance}")
            else:
                print("Insufficient balance!")
        else:
            print("Invalid amount. Please enter a number.")

    def display_account_info(self):
        print(f"Account ID: {self.account_id}\nAccount Type: {self.account_type}\nBalance: {self.balance}\n")

class SavingsAccount(Account):
    INTEREST_RATE = 0.045  # 4.5% Interest

    def __init__(self, account_id, balance=0.0):
        super().__init__(account_id, "Savings", balance)

    def calculate_interest(self):
        interest = self.balance * self.INTEREST_RATE
        self.balance += interest
        self.save_to_db()
        print(f"Interest added: {interest}. New Balance: {self.balance}")

class CurrentAccount(Account):
    OVERDRAFT_LIMIT = 5000.0

    def __init__(self, account_id, balance=0.0):
        super().__init__(account_id, "Current", balance)

    def withdraw(self, amount):
        if isinstance(amount, (int, float)):
            if self.balance - float(amount) >= -self.OVERDRAFT_LIMIT:
                self.balance -= float(amount)
                self.save_to_db()
                print(f"Withdrawn {amount}. New Balance: {self.balance}")
            else:
                print(f"Overdraft limit exceeded! You can withdraw up to {self.OVERDRAFT_LIMIT} beyond balance.")
        else:
            print("Invalid amount. Please enter a number.")

class Bank:
    @staticmethod
    def create_account():
        """Creates an account based on user choice (Savings or Current)."""
        print("Choose Account Type:\n1. Savings Account\n2. Current Account")
        choice = input("Enter choice (1 or 2): ")
        balance = float(input("Enter Initial Balance: "))

        cursor.execute("INSERT INTO accounts (account_type, balance) VALUES (%s, %s)",
                       ("Savings" if choice == "1" else "Current", balance))
        conn.commit()
        account_id = cursor.lastrowid

        if choice == "1":
            account = SavingsAccount(account_id, balance)
        elif choice == "2":
            account = CurrentAccount(account_id, balance)
        else:
            print("Invalid choice!")
            return None

        print(f"Account Created Successfully! Account ID: {account_id}")
        return account

    @staticmethod
    def perform_operations():
        account_id = input("Enter Account ID: ")

        cursor.execute("SELECT account_type, balance FROM accounts WHERE account_id = %s", (account_id,))
        result = cursor.fetchone()

        if result:
            acc_type, balance = result
            account = SavingsAccount(account_id, balance) if acc_type == "Savings" else CurrentAccount(account_id,
                                                                                                       balance)

            while True:
                print("\nBanking System Menu:")
                print("1. Deposit\n2. Withdraw\n3. Calculate Interest (Savings Only)\n4. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)
                elif choice == "2":
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)
                elif choice == "3" and isinstance(account, SavingsAccount):
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
