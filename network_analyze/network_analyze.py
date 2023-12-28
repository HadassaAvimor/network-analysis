from network_analyze import device_analyze, capture_reader
from db_management.insert_to_db import insert_to_device, insert_to_network, insert_to_devices_connections
from network_analyze.device_analyze import get_vendor
from handle_exception import HandleException
from utils.logger_handler import log
import db_management.get_from_db
from network_analyze.visualization import visualize_network


@HandleException
@log
def capture_analyze(capture_file):
    """
    A function that performs analysis of a network from a cap file.
    :param capture_file: file to analyze.
    :return: list[Dict[network_detail : detail]]
    """
    return capture_reader.extract_network_information(capture_file)


@HandleException
@log
async def create_network(capture_file, client_id, location_name):
    """
    A function that creates a network from capture file and all details.
   :param capture_file: file to analyze.
   :param client_id:
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
    network_visualisation = visualize_network(connections_list_to_db, devices_list_to_db)

    return network_id, network_visualisation


@HandleException
@log
async def add_devices_to_db(devices_list, network_id):
    devices = []
    for device in devices_list:
        vendor = await get_vendor(device)
        devices.append({'Vendor': vendor, 'MACAddress': device, 'NetworkId': network_id})
    insert_to_device(devices)


@HandleException
@log
async def add_connections_to_db(connections_list):
    connections = []
    for connection in connections_list:
        connections.append({'SourceId': connection.get('src_mac'), 'DestinationId': connection.get('dst_mac'),
                            'Protocol': connection.get('protocol')})
    insert_to_devices_connections(connections)


async def get_network_by_id(network_id):
    return db_management.get_from_db.get_network_by_network_id(network_id)
    pass
