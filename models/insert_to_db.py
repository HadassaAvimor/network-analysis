from DB_connection import insert_row_to_db, insert_many_to_db


def insert_to_network(network):
    """
    A function that insert network to the db
    :param network: dict['ClientId': client_id, 'Location': location_name, 'Date': date_taken]
    :return: network's id
    """
    return insert_row_to_db('Network', network)


def insert_to_clients(client):
    """
    A function that insert client to the db
    :param client: dict['Name': client_id, 'Location': location_name, 'Date': date_taken]
    :return: client's id
    """
    return insert_row_to_db('Clients', client)


def insert_to_technician(technician):
    """
    A function that insert technician to the db
    :param technician: dict['Name': technician_id, 'Location': location_name, 'Date': date_taken]
    :return: client's id
    """

    return insert_row_to_db('Technician', technician)


def insert_to_device(devices_list):
    """
    A function that insert device to the db
    :param devices_list: list[dict['Vendor': vendor_name, 'MACAddress': mac_address, 'NetworkId': network_id, 'Type': type]
    :return: device's id
    """
    insert_many_to_db('Device', devices_list)