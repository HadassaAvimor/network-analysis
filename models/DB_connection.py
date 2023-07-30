import os

import mysql.connector
from mysql.connector import Error

load_dotenv()


def create_server_connection(host_name, user_name, user_password, database):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
    user=os.environ["DB_USERNAME"],
    password=os.environ["DB_PASSWORD"],
    db=os.environ["DB"],
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


db_connection = create_server_connection(HOST, USER, PASSWORD, DATABASE)

