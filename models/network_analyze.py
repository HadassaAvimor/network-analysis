from models import capture_reader


def capture_analyze(capture_file):
    """
    A function that performs analysis of a network from a cap file.
    :param capture_file: file to analyze.
    :return: Dict[network_detail : detail]
    """
    packets = capture_reader.extract_network_information(capture_file)
    return packets


def normal_packets_to_analyze(packets_list):
    """
    A function that normalizes the packet data to fit the device_analyze.
    :param packets_list: List[Packet]
    :return: List[Dict[traffic_detail, detail]]
    """
    pass


# הפרמטר מורכב מהפרטים של מה שחזר מהנרמול + מה שחזר מה read_capture - הסורס והדסטיניישן
def create_network(network_information):
    """
    A function that creates a network from a dictionary of information about the network.
    :param network_information: Dict[network_detail : detail]
    :return: דיקט שמוכן להכנס לדאטה בייס
    """
    pass
