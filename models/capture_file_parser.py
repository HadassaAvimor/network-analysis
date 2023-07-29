from scapy.libs.six import BytesIO
from scapy.utils import rdpcap


def get_capture_packets_from_pcap(pcap_file):
    """
    A function that extract the packets from a pcap file.
    :param pcap_file: pcap file to extract from.
    :return: List[Packet]
    """
    file_content = BytesIO(pcap_file)
    packets = rdpcap(file_content)
    return packets




