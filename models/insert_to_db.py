from models.DB_connection import insert_row_to_db, insert_many_to_db


def insert_to_network(network):
    """
    A function that insert network to the db
    :param network: dict['ClientId': client_id, 'Location': location_name, 'Date': date_taken]
    :return: network's id
    """
    print(network)
    return insert_row_to_db('Network', network)


def insert_to_clients(client):
    """
    A function that insert client to the db
    :param client: dict['Name': client_id, 'Location': location_name, 'Date': date_taken]
    :return: client's id
    """
    return insert_row_to_db('Clients', client)


def insert_to_device(devices_list):
    """
    A function that insert devices into db
    :param devices_list: list[dict['Vendor': vendor_name, 'MACAddress': mac_address, 'NetworkId': network_id, 'Type': type]
    :return: devices ids
    """
    insert_many_to_db('Device', devices_list)


def insert_to_devices_connections(connections_list):
    """
    A function that insert connections into db
    :param connections_list: list[dict['SourceId': source_mac, 'DestinationId': destination_mac, 'Protocol': protocol]
    :return: connections ids
    """
    insert_many_to_db('Devices_connections', connections_list)

