import mysql.connector

db = mysql.connector.connect(
    host="172.17.0.2",
    user="root",
    password="password"
    )

if db.is_connected():
    print("Connected to MySQL server")
else:
    print("Failed to connect to MySQL server")

db.close()

# mycursor = db.cursor()
# mycursor.execute("CREATE DATABASE testdb")    