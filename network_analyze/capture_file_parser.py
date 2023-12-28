from scapy.libs.six import BytesIO
from scapy.utils import rdpcap, ERFEthernetReader
from handle_exception import HandleException
from utils.logger_handler import log


@HandleException
@log
def get_capture_packets_from_pcap(pcap_file):
    file_content = BytesIO(pcap_file)
    return rdpcap(file_content)


@HandleException
@log
def get_capture_packets_from_erf(erf_file):
    file_content = BytesIO(erf_file)
    return ERFEthernetReader(file_content)
