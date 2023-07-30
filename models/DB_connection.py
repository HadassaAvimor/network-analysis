import os

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()


def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="sql6.freemysqlhosting.net",
            user=os.environ["DB_USERNAME"],
            password=os.environ["DB_PASSWORD"],
            db=os.environ["DB"],
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


db_connection = create_server_connection()
