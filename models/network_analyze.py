from models import capture_reader


def capture_analyze(capture_file):
    """
    A function that performs analysis of a network from a cap file.
    :param capture_file: file to analyze.
    :return: list[Dict[network_detail : detail]]
    """
    return capture_reader.extract_network_information(capture_file)


def create_network(capture_file, client_id, date_taken, location_name):
    """
    A function that creates a network from capture file and all details.
   :param capture_file: file to analyze.
   :param client_id:
   :param date_taken:
   :param location_name: location of network
   :return: id of created network
   """
    network_info, capture_time = capture_analyze(capture_file)
    network_id = insert_to_network(
        {'ClientId': client_id, 'Location': location_name, 'Date': capture_time})
    devices_list_to_db = device_analyze.find_devices(network_info)
    connections_list_to_db = device_analyze.find_devices_connections(network_info)
    await add_devices_to_db(devices_list_to_db, network_id)
    await add_connections_to_db(connections_list_to_db)
    return network_id




async def add_connections_to_db(connections_list):
    connections = []
    for connection in connections_list:
        connections.append({'SourceId': connection.get('src_mac'), 'DestinationId': connection.get('dst_mac'),
                            'Protocol': connection.get('protocol')})
    insert_to_devices_connections(connections)
