import mysql.connector

# Establish the database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="schoolapp"
)

print("Database connection:", db)

