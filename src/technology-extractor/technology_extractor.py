import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))  # TODO: cambia e installa pacchetto

import json 
import pandas as pd

from starlink_interface import StarlinkInterface
from cellular_line_extractor import CellularLineExtractor
from broadband_extractor import BroadbandExtractor


def read_json(path) -> dict:
    """
    Legge un file JSON e lo converte in un dizionario.

    Args:
        percorso_file (str): Il percorso al file JSON.

    Returns:
        dict: I dati JSON convertiti in un dizionario.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            dati = json.load(file)
        return dati
    except FileNotFoundError:
        print(f"Errore: Il file '{path}' non è stato trovato.")
    except json.JSONDecodeError as e:
        print(f"Errore nella decodifica del file JSON: {e}")
    except Exception as e:
        print(f"Si è verificato un errore: {e}")


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
        self.broadband_extractor = BroadbandExtractor(dataset_path=self.dataset_broadband_path)
        self.cellular_line_extractor = CellularLineExtractor(dataset_path=self.dataset_cellular_line_path)
    
    def is_starlink_avaiable(self, province: str, state: str, latitude: float, longitude: float) -> bool:
        return self.starlink_interface.get_starlink_avaiability(province=province, state=state)
    
    def is_broadband_avaiable(self, province: str, state: str, latitude: float, longitude: float) -> bool:
        pass

    def get_technologies_avaiable(self,
                                  province: str,
                                  state: str,
                                  latitude_school: float,
                                  longitude_school: float,
                                  name_school: str,
                                  id_school: str,
                                  tolerance_broadband=5,
                                  tolerance_cellular_line=15) -> pd.DataFrame:
        df_broadband = self.broadband_extractor.get_broadband_availability(id_school, name_school, latitude_school, longitude_school, tolerance=tolerance_broadband)
        df_cellular_line = self.cellular_line_extractor.get_cellular_line_availability(id_school, name_school, latitude_school, longitude_school, tolerance=tolerance_cellular_line)
        df_combined = pd.concat([df_broadband, df_cellular_line], ignore_index=True)
        return df_combined
        
if __name__ == '__main__':
    technology_extractor_config = read_json('config/technology_extractor_config.json')
    technology_extractor = TechnologyExtractor(technology_extractor_config)
    data = technology_extractor.get_technologies_avaiable(id_school='id_prova',
                                                          name_school='nome_prova',
                                                          province='prova',
                                                          state='prova',
                                                          latitude_school=-2.147799969,
                                                          longitude_school=29.939599990844727,
                                                          tolerance_broadband=5,
                                                          tolerance_cellular_line=10)
    print(data)
