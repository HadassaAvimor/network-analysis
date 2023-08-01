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
   :return: מידע שמוכן להכנס לדאטה בייס
   """
    network_info = capture_analyze(capture_file)
    network_to_db = {'ClientId': client_id, 'Location': location_name, 'Date': date_taken}
    # שליחה לדאטא בייס,network לקבל את
    network_id = 'blabla'
    devices_list_to_db = []
    connections_list_to_db = []
    for connection in network_info:
        connection = {'src_mac': connection.get('src_mac'), 'des_mac': connection.get('des_mac')}
        device = {'mac_address': connection.get('src_mac'), 'network_id': network_id}
        if connection not in connections_list_to_db:
            connections_list_to_db.append(connection)
        if device not in devices_list_to_db:
            devices_list_to_db.append(device)
    # להכניס את connections and devices to the DB
    # לסדר את מה שיחזור מהדיבי
    return  # להחזיר את נטוורק המסודר


def insert_network_to_db(network, devices, connections):
    pass
