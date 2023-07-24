from abc import abstractmethod
import abc


class NetworkTrafficReader(abc):
    @staticmethod
    @abstractmethod
    def get_devices_connections(capture_file):
        """
        A function that receives a cap file and returns a list of connections between devices.
        :param capture_file: capture file to analyze
        :return: devices connections : list of tuples
        """
        pass

    @staticmethod
    @abstractmethod
    def extract_network_details(self):
        pass
