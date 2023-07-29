from models import capture_file_parser


def extract_network_information(capture_file):
    """
    A function that receives a cap file and returns a dictionary that contains information of the packets.
    :param capture_file: capture file to analyze
    :return: network information : List[Dict[detail : information]]
    """
    network = file_classification(capture_file)
    return network


def file_classification(capture_file):
    """
    A function that classifies the capture file according its type, and sends to the suitable processing for it.
    :param capture_file: capture file to classify.
    :return: List[Packet]
    """
    extension = capture_file.filename.split(".")[-1]
    match extension:
        case 'pcap':
            return capture_file_parser.get_capture_packets_from_pcap(capture_file.file.read())
        case 'pcapng':
            return capture_file_parser.get_capture_packets_from_pcap(capture_file.file.read())
        case 'cap':
            pass
        case 'erf':
            pass
    raise ValueError("Unsupported file extension: {}".format(extension))


