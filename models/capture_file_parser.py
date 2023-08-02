from scapy.libs.six import BytesIO
from scapy.utils import rdpcap
from handle_exception import HandleException

@log
@HandleException
def get_capture_packets_from_pcap(pcap_file):
    file_content = BytesIO(pcap_file)
    return rdpcap(file_content)
