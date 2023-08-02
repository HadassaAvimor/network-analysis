from DB_connection import get_cursor

cursor = get_cursor()


def get_all_by_table_name(table_name):
    select_all = f"SELECT * FROM {table_name}"
    cursor.execute(select_all)
    return cursor.fetchall()


def get_one_by_condition(table_name, **kwargs):
    select_query = create_query_by_filter(table_name, "SELECT *", **kwargs)
    cursor.execute(select_query)
    return cursor.fetchone()


def get_many_by_condition(table_name, **kwargs):
    query = create_query_by_filter(table_name, "SELECT *", **kwargs)
    cursor.execute(query)
    return cursor.fetchall()


def create_query_by_filter(table_name, base_query, **kwargs):
    query = f"{base_query} FROM {table_name} WHERE"
    for key, value in kwargs.items():
        if type(value) is str and not value.isdigit():
            value = f"'{value}'"
        query += f" {key}={value} AND "
    return query[:-5]


def select_by_query(query):
    cursor.execute(query)
    return cursor.fetchall()


# def filter_data_by_columns(data_dict):
#     result_data = {}
#     for table_name, column_name, column_order, values in zip(data_dict['table_name'], data_dict['column_name'],
#                                                              data_dict['columns_order'], data_dict['value']):
#         order = ''
#         for column in column_order:
#             order += column
#             order += ' ,'
#         order = order[:-1]
#         select_query = f"SELECT {order} FROM {table_name} WHERE {column_name} = %s"
#         table_results = {}
#         cursor.execute(select_query, (values,))
#         rows = cursor.fetchall()
#         print(column_order, rows)
#         for name, value in zip(column_order, rows):
#             table_results[name] = value
#         result_data[table_name] = table_results
#
#     return result_data


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


def get_all_devices(network_id):
    query = f'''SELECT Device.MACAddress, Device.vendor 
                           FROM Network 
                           LEFT JOIN Device ON Network.Id = Device.NetworkId 
                           WHERE Network.Id = {network_id}'''
    return select_by_query(query)


def get_devices_by_client_id(client_id):
    query = f"""SELECT d.MACAddress FROM Device d 
                           JOIN Network n 
                           ON d.NetworkId = n.Id WHERE n.ClientId = {client_id} """
    return select_by_query(query)


def get_devices_by_vendor(network_id, vendor):
    devices = get_all_devices(network_id)
    return [device for device in devices if device[1] == vendor]


def get_communication(network_id):
    query = 'SELECT Device.NetworkId, Devices_connections.SourceId, Devices_connections.DestinationId' \
            ' FROM Devices_connections ' \
            'LEFT JOIN Device ON SourceId = Device.MACAddress ' \
            f'WHERE Device.NetworkId = {network_id}'
    return select_by_query(query)