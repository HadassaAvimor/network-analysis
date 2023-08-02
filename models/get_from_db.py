from DB_connection import get_cursor
from normal_data_from_db import normal_communication, normal_network_details
from handle_exception import HandleException
from logger_handler import log

cursor = get_cursor()


@HandleException
@log
def get_all_by_table_name(table_name):
    select_all = f"SELECT * FROM {table_name}"
    cursor.execute(select_all)
    return cursor.fetchall()


@HandleException
@log
def get_one_by_condition(table_name, **kwargs):
    select_query = create_query_by_filter(table_name, "SELECT *", **kwargs)
    cursor.execute(select_query)
    return cursor.fetchone()


@HandleException
@log
def get_many_by_condition(table_name, **kwargs):
    query = create_query_by_filter(table_name, "SELECT *", **kwargs)
    cursor.execute(query)
    return cursor.fetchall()


@HandleException
@log
def create_query_by_filter(table_name, base_query, **kwargs):
    query = f"{base_query} FROM {table_name} WHERE"
    for key, value in kwargs.items():
        if type(value) is str and not value.isdigit():
            value = f"'{value}'"
        query += f" {key}={value} AND "
    return query[:-5]


@HandleException
@log
def select_by_query(query):
    cursor.execute(query)
    return cursor.fetchall()


@HandleException
@log
def get_network_by_network_id(network_id):
    query = f"""SELECT Network.Date, Network.Location, Clients.Name, Device.MACAddress, Device.Vendor,
                           Devices_connections.SourceId, Devices_connections.DestinationId
                           FROM Network
                           INNER JOIN Clients
                           ON Network.ClientId = Clients.Id
                           LEFT JOIN (
                           SELECT MACAddress, NetworkId , Vendor
                           FROM Device WHERE NetworkId = {network_id} )
                           AS Device ON Network.Id = Device.NetworkId
                           LEFT JOIN Devices_connections
                           ON Device.MACAddress = Devices_connections.SourceId
                           WHERE NetworkId = {network_id}"""
    return select_by_query(query)


@HandleException
@log
def get_all_devices(network_id):
    query = f'''SELECT Device.MACAddress, Device.vendor 
                           FROM Network 
                           LEFT JOIN Device ON Network.Id = Device.NetworkId 
                           WHERE Network.Id = {network_id}'''
    data_from_db = select_by_query(query)
    return normal_network_details(data_from_db)


@HandleException
@log
def get_devices_by_client_id(client_id):
    query = f"""SELECT d.MACAddress FROM Device d 
                           JOIN Network n 
                           ON d.NetworkId = n.Id WHERE n.ClientId = {client_id} """
    return select_by_query(query)


@HandleException
@log
def get_devices_by_vendor(network_id, vendor):
    devices = get_all_devices(network_id)
    return [device for device in devices if device[1] == vendor]


@HandleException
@log
def get_communication(network_id):
    query = 'SELECT Device.NetworkId, Devices_connections.SourceId, Devices_connections.DestinationId' \
            ' FROM Devices_connections ' \
            'LEFT JOIN Device ON SourceId = Device.MACAddress ' \
            f'WHERE Device.NetworkId = {network_id}'
    data_from_db = select_by_query(query)
    return normal_communication(data_from_db)


@HandleException
@log
def get_technician(**kwargs):
    data_from_db = get_one_by_condition('Technicians', **kwargs)
    return normal_communication(data_from_db)
