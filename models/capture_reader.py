import time
from scapy.contrib.rtcp import RTCP
from scapy.layers.inet import IP, TCP, UDP
from scapy.layers.l2 import ARP
from scapy.layers.ntp import NTP
from handle_exception import HandleException
from models.logger_handler import log
from models.capture_file_parser import get_capture_packets_from_erf, get_capture_packets_from_pcap


@HandleException
@log
def extract_time_from_packet(packet):
    timestamp = packet.time
    local_time = time.localtime(int(timestamp))
    return time.strftime("%Y-%m-%d", local_time)


@HandleException
@log
def extract_network_information(capture_file):
    """
    A function that receives a cap file and returns a dictionary that contains information of the packets.
    :param capture_file: capture file to analyze
    :return: network information : List[Dict[detail : information]], capture_time
    """
    packets = file_classification(capture_file)
    network = []
    time_taken = extract_time_from_packet(packets[0])

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

    return network, time_taken


@HandleException
@log
def file_classification(capture_file):
    """
    A function that classifies the capture file according its type, and sends to the suitable processing for it.
    :param capture_file: capture file to classify.
    :return: List[Packet]
    """
    extension = capture_file.filename.split(".")[-1]
    cap_file = capture_file.file.read()
    match extension:
        case 'pcap':
            return get_capture_packets_from_pcap(cap_file)
        case 'pcapng':
            return get_capture_packets_from_pcap(cap_file)
        case 'cap':
            return get_capture_packets_from_pcap(cap_file)
        case 'erf':
            get_capture_packets_from_erf(cap_file)

    raise ValueError("Unsupported file extension: {}".format(extension))

