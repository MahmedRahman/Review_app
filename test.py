import MySQLdb

try:
    connection = MySQLdb.connect(
        user='atpfreelancer',
        passwd='atp5797895',
        host='atpfreelancer.mysql.pythonanywhere-services.com',
        db='atpfreelancer$eva',
    )

    cursor = connection.cursor()
    cursor.execute("SELECT 1")  # Run a simple query
    result = cursor.fetchone()
    if result is not None:
        print("Connected to the database")
    else:
        print("Failed to connect to the database")
    
    # Do stuff

finally:
    connection.close()
