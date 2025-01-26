import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))  # TODO: cambia e installa pacchetto

import pandas as pd

from technology_extractor.technology_extractor import TechnologyExtractor, read_json
from schools_extractor.schools_extractor import SchoolsExtractor

base_report_path = 'report'
import os
from datetime import datetime

def create_folder_with_timestamp(base_path):
    # Ottieni il timestamp attuale come stringa
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Crea il percorso della cartella
    folder_path = os.path.join(base_path, timestamp)
    
    # Crea la cartella
    os.makedirs(folder_path, exist_ok=True)
    
    print(f"Cartella creata: {folder_path}")
    return folder_path


def save_settings(choosen_country: str, budget: float, folder_path: str, filename: str):
    import json
    file_path = os.path.join(folder_path, filename)
    settings = {
        "choosen_country": choosen_country,
        "budget": budget
    }
    
    with open(file_path, 'w') as json_file:
        json.dump(settings, json_file, indent=4)
    print(f"File salvato come {file_path}")


def write_data_to_csv(data: pd.DataFrame, folder_path: str, filename: str):
    filepath = os.path.join(folder_path, filename)
    data_rounded = data.applymap(lambda x: round(x, 4) if isinstance(x, float) else x)
    data_rounded = data_rounded.drop(columns=['id_school'])
    data_rounded.to_csv(filepath)


if __name__ == '__main__':
    folder_path = create_folder_with_timestamp(base_path=base_report_path)
    choosen_country = 'Rwanda'
    budget = 30000
    unconnected_school_extractor = SchoolsExtractor('data\school_geolocations_with-connnectivity.csv')
    data = unconnected_school_extractor.get_unconnected_schools(choosen_country)
    save_settings(choosen_country, budget, folder_path, "settings.json")

    unconnected_schools = data.head(50)
    technology_extractor_config = read_json('config/technology_extractor_config.json')
    technology_extractor = TechnologyExtractor(technology_extractor_config)
    technology_extractor.initalize_disconnected_schools(unconnected_schools)
    data = technology_extractor.get_df_technologies_avaiable_for_disconnected_schools()
    write_data_to_csv(data, folder_path, filename='unconnected_schools_technology.csv')