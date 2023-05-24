import MySQLdb
import sshtunnel

sshtunnel.SSH_TIMEOUT = 5.0
sshtunnel.TUNNEL_TIMEOUT = 5.0

with sshtunnel.SSHTunnelForwarder(
    ('ssh.pythonanywhere.com'),
    ssh_username='atpfreelancer', ssh_password='atp5797895',
    remote_bind_address=('atpfreelancer.mysql.pythonanywhere-services.com', 3306)
) as tunnel:
    connection = MySQLdb.connect(
        user='atpfreelancer',
        passwd='atp5797895',
        host='127.0.0.1', port=tunnel.local_bind_port,
        db='atpfreelancer$eva',
    )
    # Do stuff
    connection.close()
