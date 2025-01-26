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
        self._initalize_disconnected_schools()
    
    def _initalize_disconnected_schools(self):
        self.disconnected_schools = [{'id_school':'school_1', 'name_school': 'school1_name', 'lat': -1.88, 'lon': 29.5},
                                    {'id_school':'school_2', 'name_school': 'school2_name', 'lat': -1.78, 'lon': 31.5},
                                    {'id_school':'school_3', 'name_school': 'school3_name', 'lat': -1.98, 'lon': 28.5},
                                    {'id_school':'school_4', 'name_school': 'school4_name', 'lat': -1.765, 'lon': 27.5},
                                    {'id_school':'school_5', 'name_school': 'school5_name', 'lat': -1.68, 'lon': 31.5}]

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

    def get_df_technologies_avaiable_for_disconnected_schools(self) -> pd.DataFrame:
        """
        Ritorna un dataframe con le seguenti colonne
        "   id_school   name_school  latitude_school  longitude_school type_technology  latitude_service_point  longitude_service_point tower_range_meters  distance_km_school_service_point"
        In cui tiene le informazioni che per ogni scuola le tecnologie disponibili nelle vicinanze
        """
        dataframes = []
        for el in self.disconnected_schools:
            data = technology_extractor.get_technologies_avaiable(id_school=el['id_school'],
                                                                name_school=el['name_school'],
                                                                province='prova',
                                                                state='prova',
                                                                latitude_school=el['lat'],
                                                                longitude_school=el['lon'],
                                                                tolerance_broadband=15,
                                                                tolerance_cellular_line=25)
            dataframes.append(data)
        return pd.concat(dataframes, ignore_index=True)
            
if __name__ == '__main__':"
    technology_extractor_config = read_json('config/technology_extractor_config.json')
    technology_extractor = TechnologyExtractor(technology_extractor_config)
    data = technology_extractor.get_df_technologies_avaiable_for_disconnected_schools()
    print(data)