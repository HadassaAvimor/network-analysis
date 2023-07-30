from scapy.contrib.rtcp import RTCP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import ARP
from scapy.layers.ntp import NTP

from models import capture_file_parser


def extract_network_information(capture_file):
    """
    A function that receives a cap file and returns a dictionary that contains information of the packets.
    :param capture_file: capture file to analyze
    :return: network information : List[Dict[detail : information]]
    """
    packets = file_classification(capture_file)
    network = []
    for packet in packets:
        details_dict = {'src_mac': packet.src, 'dst_mac': packet.dst}

        protocols = [UDP, TCP, RTCP, ARP, NTP]
        for protocol in protocols:
            if protocol in packet:
                details_dict["protocol"] = packet[protocol]
                break

        if IP in packet:
            details_dict['src_IP'] = packet['IP'].src
            details_dict['dst_IP'] = packet['IP'].dst
        network.append(details_dict)

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
