from models.insert_to_db import insert_to_device, insert_to_network
from models import capture_reader, device_analyze
from mac_vendor_lookup import MacLookup


def capture_analyze(capture_file):
    """
    A function that performs analysis of a network from a cap file.
    :param capture_file: file to analyze.
    :return: list[Dict[network_detail : detail]]
    """
    return capture_reader.extract_network_information(capture_file)


def create_network(capture_file, client_id, location_name):
    """
    A function that creates a network from capture file and all details.
   :param capture_file: file to analyze.
   :param client_id:
   :param location_name: location of network
   :return: id of created network
   """
    network_info = capture_analyze(capture_file)
    network_id = insert_to_network(
        {'ClientId': client_id, 'Location': location_name, 'Date': '11122'})
    devices_list_to_db = device_analyze.find_devices(network_info)
    connections_list_to_db = device_analyze.find_devices_connections(network_info)
    add_devices_to_db(devices_list_to_db, network_id)
    return network_id


def add_devices_to_db(devices_list, network_id):
    devices = []
    for device in devices_list:
        # vendor = MacLookup().lookup(device)
        # print(vendor)
        devices.append({'Vendor': '111', 'MACAddress': device, 'NetworkId': network_id})
    print(type(devices[0]))

    print(type(devices))
    insert_to_device([{'Vendor': '111', 'MACAddress': "1", 'NetworkId': 1},
                                          {'Vendor': '111', 'MACAddress': 'device', 'NetworkId': 1}])


