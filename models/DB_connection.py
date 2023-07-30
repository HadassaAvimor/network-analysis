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
            db=os.environ["DB"]
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")
    return connection


db_connection = create_server_connection()


def insert_row(table_name, values):
    """
  Inserts a row into a table in the database.
  Args: table_name: The name of the table to insert the row into.
        values: A dict of values to insert into the table.
  Returns: the new row
  """
    cursor = db_connection.cursor()
    # Create the SQL query.
    query = "INSERT INTO %s (%s) VALUES (%s)" % (
        table_name,
        ",".join(values.keys()),
        ",".join("%s" for _ in values.values())
    )
    cursor.execute(query, tuple(values.values()))
    db_connection.commit()
    db_connection.close()
    return cursor.lastrowid


