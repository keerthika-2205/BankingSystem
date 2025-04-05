import mysql.connector

# DB connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NewPassword",
    database="banking"
)
cursor = conn.cursor()

def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long.", False
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter.", False
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one digit.", False
    return "Password is valid!", True

# Get user input
username = input("Enter your username: ")
user_password = input("Create your bank account password: ")

# Validate password
message, is_valid = validate_password(user_password)
print(message)

# If valid, insert into database
if is_valid:
    insert_query = "INSERT INTO user_passwords (username, password) VALUES (%s, %s)"
    cursor.execute(insert_query, (username, user_password))
    conn.commit()
    print("Password saved successfully in the database.")

# Close connection
cursor.close()
conn.close()
