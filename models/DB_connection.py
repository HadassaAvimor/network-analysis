import mysql.connector
from mysql.connector import Error

HOST = "sql6.freemysqlhosting.net"
USER = "sql6635129"
PASSWORD = "UD9PIExeur"
DATABASE = "sql6635129"


def create_server_connection(host_name, user_name, user_password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=database

        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


db_connection = create_server_connection(HOST, USER, PASSWORD, DATABASE)
