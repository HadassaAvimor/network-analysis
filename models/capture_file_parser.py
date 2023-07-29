from scapy.libs.six import BytesIO
from scapy.utils import rdpcap


def get_capture_packets_from_pcap(pcap_file):
    file_content = BytesIO(pcap_file)
    packets = rdpcap(file_content)
    return packets



