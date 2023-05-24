import mysql.connector

# Create connection
conn = mysql.connector.connect(
    host='localhost',  # your host, usually localhost
    user='yourusername',  # your username
    passwd='yourpassword'  # your password
)

cur = conn.cursor()

# Drop the existing database if it exists and create a new one
cur.execute("DROP DATABASE IF EXISTS SubscriptionDB")
cur.execute("CREATE DATABASE SubscriptionDB")

# Use new database
cur.execute("USE SubscriptionDB")

# Define SQL commands and execute them one by one

cur.execute("DROP TABLE IF EXISTS Invoices")
cur.execute("DROP TABLE IF EXISTS Coupons")
cur.execute("DROP TABLE IF EXISTS Logs")
cur.execute("DROP TABLE IF EXISTS UserSubscriptions")
cur.execute("DROP TABLE IF EXISTS Subscriptions")
cur.execute("DROP TABLE IF EXISTS Users")

cur.execute("""
    CREATE TABLE Users (
        UserID INT PRIMARY KEY,
        FullName VARCHAR(100),
        Email VARCHAR(100),
        Phone VARCHAR(15),
        EmailVerified BOOLEAN,
        Password VARCHAR(255),
        Status ENUM('Active', 'Inactive', 'Suspended', 'Deleted'),
        DateRegistered DATETIME
    );
""")

cur.execute("""
    CREATE TABLE Subscriptions (
        SubscriptionID INT PRIMARY KEY,
        SubscriptionName VARCHAR(50),
        SubscriptionDetails VARCHAR(255),
        Duration INT
    );
""")

cur.execute("""
    CREATE TABLE UserSubscriptions (
        UserSubscriptionID INT PRIMARY KEY,
        UserID INT,
        SubscriptionID INT,
        SubscriptionStatus ENUM('Active', 'Inactive', 'Suspended', 'Cancelled'),
        FOREIGN KEY(UserID) REFERENCES Users(UserID),
        FOREIGN KEY(SubscriptionID) REFERENCES Subscriptions(SubscriptionID)
    );
""")

cur.execute("""
    CREATE TABLE Coupons (
        CouponID INT PRIMARY KEY,
        CouponCode VARCHAR(15),
        Discount DECIMAL(10,2),
        ExpiryDate DATETIME
    );
""")

cur.execute("""
    CREATE TABLE Invoices (
        InvoiceID INT PRIMARY KEY,
        UserSubscriptionID INT,
        PaymentMethod ENUM('Credit Card', 'PayPal', 'Bank Transfer'),
        CouponCode VARCHAR(15),
        PriceBefore DECIMAL(10,2),
        PriceAfter DECIMAL(10,2),
        InvoiceDate DATETIME,
        FOREIGN KEY(UserSubscriptionID) REFERENCES UserSubscriptions(UserSubscriptionID)
    );
""")

cur.execute("""
    CREATE TABLE Logs (
        LogID INT PRIMARY KEY,
        UserID INT,
        SubscriptionID INT,
        Action VARCHAR(50),
        ActionDate DATETIME,
        Details VARCHAR(255),
        FOREIGN KEY(UserID) REFERENCES Users(UserID),
        FOREIGN KEY(SubscriptionID) REFERENCES Subscriptions(SubscriptionID)
    );
""")

# Commit changes and close connection
conn.commit()
conn.close()
