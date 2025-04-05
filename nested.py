import mysql.connector

class ATM:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",  # change if needed
            password="NewPassword",  # your MySQL password
            database="banking"  # your database name
        )
        self.cursor = self.conn.cursor()

    def record_transaction(self, customer_id, transaction_type, amount):
        query = """
        INSERT INTO transactions (transaction_type, amount, customer_id)
        VALUES (%s, %s, %s)
        """
        self.cursor.execute(query, (transaction_type, amount, customer_id))
        self.conn.commit()

    def atm_operations(self):
        customer_id = int(input("Enter your Customer ID: "))
        balance = float(input("Enter your Current Balance: "))

        print("\n--- ATM Menu ---")
        print("1. Check Balance")
        print("2. Withdraw")
        print("3. Deposit")

        choice = input("Choose an option (1-3): ")

        if choice == "1":
            print(f"Your current balance is: ${balance:.2f}")
        elif choice == "2":
            amount = float(input("Enter amount to withdraw: "))
            if amount > balance:
                print(" Insufficient Balance!")
            else:
                if amount % 100 == 0 or amount % 500 == 0:
                    balance -= amount
                    print(f"Withdrawal Successful! New Balance: ${balance:.2f}")
                    self.record_transaction(customer_id, "Withdraw", amount)
                else:
                    print("Amount must be in multiples of 100 or 500.")
        elif choice == "3":
            amount = float(input("Enter amount to deposit: "))
            balance += amount
            print(f"Deposit Successful! New Balance: ${balance:.2f}")
            self.record_transaction(customer_id, "Deposit", amount)
        else:
            print("Invalid choice. Please try again.")

        self.cursor.close()
        self.conn.close()

# Run the ATM simulation
atm = ATM()
atm.atm_operations()
