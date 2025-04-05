from bean.Customer import Customer
from service.BankServiceProviderImpl import BankServiceProviderImpl


bank = BankServiceProviderImpl("HexaBank", "Chennai")

def main():
    while True:
        print("\n--- Bank Menu ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Get Balance")
        print("5. Transfer")
        print("6. Get Account Details")
        print("7. List Accounts")
        print("8. Exit")

        choice = input("Enter choice: ")

        if choice == '1':
            fname = input("First Name: ")
            lname = input("Last Name: ")
            email = input("Email: ")
            phone = input("Phone: ")
            address = input("Address: ")
            acc_type = input("Account Type (Savings/Current/ZeroBalance): ")
            balance = float(input("Initial Balance: "))

            customer = Customer(None, fname, lname, email, phone, address)
            bank.create_account(customer, acc_type, balance)
            print("Account created successfully!")

        elif choice == '2':
            acc = int(input("Account Number: "))
            amt = float(input("Amount to deposit: "))
            print("New Balance:", bank.deposit(acc, amt))

        elif choice == '3':
            acc = int(input("Account Number: "))
            amt = float(input("Amount to withdraw: "))
            print("New Balance:", bank.withdraw(acc, amt))

        elif choice == '4':
            acc = int(input("Account Number: "))
            print("Balance:", bank.get_account_balance(acc))

        elif choice == '5':
            from_acc = int(input("From Account: "))
            to_acc = int(input("To Account: "))
            amt = float(input("Amount: "))
            bank.transfer(from_acc, to_acc, amt)
            print("Transfer successful.")

        elif choice == '6':
            acc = int(input("Account Number: "))
            print("Details:", bank.get_account_details(acc))

        elif choice == '7':
            for acc in bank.list_accounts():
                print(acc)

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid option.")

if __name__ == '__main__':
    main()