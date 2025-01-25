import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))  # TODO: cambia e installa pacchetto

from starlink_interface import StarlinkInterface


class TechnologyExtractor:
    """
    Questo modulo si occupa di prendere le informazioni riguardanti le tecnologie disponibili in una determinata posizione (latitudine, longitudine) e ritornare un dizionario con le informazioni
    """
    def __init__(self,
                 config: dict):
        self.config = config
        self.dataset_broadband_path = self.config['dataset_broadband_path']
        self.dataset_cellular_line_path = self.config['dataset_cellular_line_path']
        self.dataset_starlink_path = self.config['dataset_starlink_path']
        self.starlink_interface = StarlinkInterface(dataset_path=self.dataset_starlink_path)
    
    def is_starlink_avaiable(self, province: str, state: str, latitude: float, longitude: float) -> bool:
        return self.starlink_interface.get_starlink_avaiability(province=province, state=state)
    
    def is_broadband_avaiable(self, province: str, state: str, latitude: float, longitude: float) -> bool:
        pass

    def is_cellular_line_avaiable(self, province: str, state: str, latitude: float, longitude: float) -> bool:

    def get_technologies_avaiable(self, province: str, state: str, latitude: float, longitude: float) -> dict:
        
        pass
