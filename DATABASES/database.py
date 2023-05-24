import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",  # your host, usually localhost
  user="root",  # your username
  password="12345678"  # your password
)

print(mydb)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE eva")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="12345678",
  database="eva"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), email VARCHAR(255))")

sql = "INSERT INTO users (name, email) VALUES (%s, %s)"
val = ("John", "john@example.com")
mycursor.execute(sql, val)

mydb.commit()

print(mycursor.rowcount, "record inserted.")
