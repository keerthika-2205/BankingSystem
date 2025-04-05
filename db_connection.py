import mysql.connector

try:
    connection = mysql.connector.connect(
        host="localhost",  
        user="root",
        password="NewPassword",
        database="banking",
        port=3306
    )
    print(" Connected to MySQL successfully!")
except mysql.connector.Error as err:
    print(f"MySQL Error: {err}")
