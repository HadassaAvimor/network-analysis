import os
from handle_exception import HandleException

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from logger_handler import log

load_dotenv()


@log
@HandleException
def create_server_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host="sql6.freemysqlhosting.net",
            user=os.environ["DB_USERNAME"],
            password=os.environ["DB_PASSWORD"],
            db=os.environ["DB"]
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


db_connection = create_server_connection()
cursor = db_connection.cursor()


@log
@HandleException
def connect_to_db(query, values_tuple):
    if isinstance(values_tuple, list):
        cursor.executemany(query, values_tuple)
    else:
        cursor.execute(query, values_tuple)
    db_connection.commit()
    return cursor.lastrowid
