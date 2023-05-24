import MySQLdb

connection = MySQLdb.connect(
    user='atpfreelancer',
    passwd='atp5797895',
    host='atpfreelancer.mysql.pythonanywhere-services.com',
    db='atpfreelancer$eva',
)

# Do stuff

connection.close()
