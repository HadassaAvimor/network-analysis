import httpx
from handle_exception import HandleException
from models.logger_handler import log


@HandleException
@log
def find_devices(traffic_list):
    """
     A function that finds connections between devices in a pcap file.
    :param traffic_list: list of Dict[traffic_detail, detail]
    :return: List[Dict[src_mac, dst_mac]].
    """
    devices_list = []
    for traffic in traffic_list:
        device = traffic.get('src_mac')
        if device not in devices_list:
            devices_list.append(device)
    return devices_list


@HandleException
@log
def find_devices_connections(traffic_list):
    """
     A function that finds connections between devices in a pcap file.
    :param traffic_list: List[Dict[traffic_detail, detail]]
    :return: Dict[mac_source, destination_source, protocol].
    """
    connections_list = []
    for connection in traffic_list:
        connection = {'src_mac': connection.get('src_mac'), 'dst_mac': connection.get('dst_mac'),
                      'protocol': str(connection.get('protocol'))}
        if connection not in connections_list:
            connections_list.append(connection)
    return connections_list


@HandleException
@log
async def get_vendor(mac_address):
    """
    A function that finds the vendor of device by mac address
    :param mac_address: device's mac address
    :return: vendor of mac address
    """
    url = f"https://api.macvendors.com/{mac_address}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPError:
            return None
