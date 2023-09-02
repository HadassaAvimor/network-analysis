import os
from handle_exception import HandleException

import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error
from models.logger_handler import log

load_dotenv()


@HandleException
@log
def create_server_connection():
    connection = None

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="a24h68",
        db="NA"
    )

    return connection


db_connection = create_server_connection()
cursor = db_connection.cursor()


def get_cursor():
    return cursor


@HandleException
@log
def connect_to_db(query, values_tuple):
    if isinstance(values_tuple, list):
        cursor.executemany(query, values_tuple)
    else:
        cursor.execute(query, values_tuple)
    db_connection.commit()
    return cursor.lastrowid



