import mysql.connector

class CompoundInterestCalculator:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="NewPassword",  # Replace with your password
            database="banking"      # Replace with your DB name
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS interest_calculations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(100),
            initial_balance FLOAT,
            annual_interest_rate FLOAT,
            years INT,
            future_balance FLOAT
        )
        """
        self.cursor.execute(query)
        self.conn.commit()

    def calculate_and_store_interest(self, customer_name, balance, rate, years):
        future_balance = balance * ((1 + rate / 100) ** years)
        query = """
        INSERT INTO interest_calculations (customer_name, initial_balance, annual_interest_rate, years, future_balance)
        VALUES (%s, %s, %s, %s, %s)
        """
        self.cursor.execute(query, (customer_name, balance, rate, years, future_balance))
        self.conn.commit()
        return future_balance

    def close(self):
        self.cursor.close()
        self.conn.close()

# ---------- Main Program ----------
if __name__ == "__main__":
    calc = CompoundInterestCalculator()
    num_customers = int(input("Enter number of customers: "))

    for i in range(num_customers):
        print(f"\nCustomer {i+1}")
        name = input("Enter Customer Name: ")
        initial_balance = float(input("Enter Initial Balance: "))
        annual_interest_rate = float(input("Enter Annual Interest Rate (%): "))
        years = int(input("Enter Number of Years: "))

        future = calc.calculate_and_store_interest(name, initial_balance, annual_interest_rate, years)
        print(f"Future Balance for {name}: ${future:.2f}")

    calc.close()
    print("\nAll records saved to the database.")
