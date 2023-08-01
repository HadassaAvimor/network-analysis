# מקבל dictionary מהמודול עם השם הארוך, ומחלץ את המידע של איזה התקן מתחבר לאיזה התקו

# מחזיר דיקט של התקנים, כל התקן עם כל הפרטים עליו

def find_devices(traffic_list):
    """
    Finds connections between devices in a pcap file.
    :param traffic_list: list of Dict[traffic_detail, detail]
    :return: List[Dict[src_mac, dst_mac]].
    """
    devices_list = []
    for traffic in traffic_list:
        device = traffic.get('src_mac')
        if device not in devices_list:
            devices_list.append(device)
    return devices_list


def find_devices_connections(traffic_list):
    """
    Finds connections between devices in a pcap file.
    :param traffic_list: List[Dict[traffic_detail, detail]]
    :return: Dict[mac_source, destination_source].
    """
    connections_list = []
    for connection in traffic_list:
        connection = {'src_mac': connection.get('src_mac'), 'dst_mac': connection.get('dst_mac')}
        if connection not in connections_list:
            connections_list.append(connection)
    return connections_list
