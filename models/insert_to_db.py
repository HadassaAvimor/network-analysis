from handle_exception import HandleException
from DB_connection import connect_to_db
from logger_handler import log


@HandleException
@log
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


@HandleException
@log
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
    return connect_to_db(query, list([list(value.values()) for value in values_list]))


@HandleException
@log
def insert_to_network(network):
    """
    A function that insert network to the db
    :param network: dict['ClientId': client_id, 'Location': location_name, 'Date': date_taken]
    :return: network's id
    """
    return insert_row_to_db('Network', network)


@HandleException
@log
def insert_to_clients(client):
    """
    A function that insert client to the db
    :param client: dict['Name': client_id, 'Location': location_name, 'Date': date_taken]
    :return: client's id
    """
    return insert_row_to_db('Clients', client)


@HandleException
@log
def insert_to_technician(technician):
    """
    A function that insert technician to the db
    :param technician: dict['Username': username, 'Password': password]
    :return: client's id
    """

    return insert_row_to_db('Technicians', technician)


@HandleException
@log
def insert_to_device(devices_list):
    """
    A function that insert device to the db
    :param devices_list: list[dict['Vendor': vendor_name, 'MACAddress': mac_address, 'NetworkId': network_id, 'Type': type]
    :return: device's id
    """
    insert_many_to_db('Device', devices_list)


@HandleException
@log
def insert_to_devices_connections(connections_list):
    """
     A function that insert connections to the db
    :param connections_list: list[dict['SourceId': src_mac, 'DestinationId': dst_mac, 'Protocol': protocol]
    :return: connections id's
    """
    insert_many_to_db('Devices_connections', connections_list)


