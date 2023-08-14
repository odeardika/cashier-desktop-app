import mysql.connector



def connect():
    return mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '125125',
        database = 'my_store', 
    )
