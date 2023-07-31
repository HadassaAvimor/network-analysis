import os
import string
import time

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
cursor = db_connection.cursor()


def connect_to_db(query, values_tuple):
    cursor.execute(query, values_tuple)
    db_connection.commit()
    db_connection.close()
    return cursor.lastrowid


def insert_row_to_db(table_name, values):
    """
  Inserts a row into a table in the database.
  Args: table_name: The name of the table to insert the row into.
        values: A dict of values to insert into the table.
  Returns: the new row's id
  """
    # Create the SQL query.
    query = "INSERT INTO %s (%s) VALUES (%s)" % (
        table_name,
        ",".join(values.keys()),
        ",".join("%s" for _ in values.values())
    )
    return connect_to_db(query, tuple(values.values()))


def insert_many_to_db(table_name, values_list):
    """
    Inserts rows into a table in the database.
    :param table_name: The name of the table to insert the row into.
    :param values_list: A list of dicts of values to insert into the table.
    :return: list of new row's ids
    """

    query = "INSERT INTO %s (%s) VALUES (%s)" % (
        table_name,
        ",".join(values_list[0].keys()),
        ",".join("%s" for _ in values_list[0].values())
    )
    print(list([list(value.values()) for value in values_list]))
    return connect_to_db(query, list([list(value.values()) for value in values_list]))


def extract_network_by_id(network_id):
    select_network_query = 'SELECT Network.Date, Network.Location, Clients.Name ' \
                           'FROM Network ' \
                           'INNER JOIN Clients ON Network.ClientId=Clients.Id ' \
                           f'WHERE Network.Id = {network_id} '
    cursor = db_connection.cursor()
    # Create the SQL query.
    query = 'SELECT Network.Date, Network.Location, Clients.Name ' \
            'FROM Network ' \
            'INNER JOIN Clients ON Network.ClientId=Clients.Id ' \
            f'WHERE Network.Id = {network_id} '

    select_network = cursor.execute(query)
    # db_connection.commit()

    db_connection.close()

    # SELECT Network.Date, Network.Location, Clients.Name, Device.MACAddress
    # FROM Network
    # INNER JOIN Clients ON Network.ClientId = Clients.Id
    # LEFT JOIN (
    #     SELECT MACAddress, NetworkId
    #     FROM Device
    #     WHERE NetworkId = {network_id}
    # ) AS Device ON Network.Id = Device.NetworkId
    # WHERE Network.Id = {network_id};

# insert_row('Network', {'ClientId': 1, 'Location': 'TLV', 'Date': time.time()})
# print(extract_network_by_id(1))
