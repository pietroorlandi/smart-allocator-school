import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))  # TODO: cambia e installa pacchetto

import pandas as pd

from technology_extractor.technology_extractor import TechnologyExtractor, read_json
from schools_extractor.schools_extractor import SchoolsExtractor
from cost_estimate_technology.technology_estimator import LLMEstimatorCost, read_file
from data_transformer.data_transformer import DataTransformer
from resource_allocator.resource_allocator import ResourceAllocator
from document_generator.document_generator import DocumentGenerator

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


def write_file_json(data, folder, filename):
    import json
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file, indent=4)


def write_file_txt(data, folder, filename):
    filepath = os.path.join(folder, filename)
    with open(filepath, 'w') as txt_file:
        for item in data:
            txt_file.write(str(item) + "\n")


def write_data_to_csv(data: pd.DataFrame, folder_path: str, filename: str):
    filepath = os.path.join(folder_path, filename)
    data_rounded = data.applymap(lambda x: round(x, 4) if isinstance(x, float) else x)
    # data_rounded = data_rounded.drop(columns=['id_school'])
    data_rounded.to_csv(filepath)
    return filepath


def run_pipeline(choosen_country: str, budget: float, api_key: str):
    """
    Ritorna un Markdown che riassume le decisioni prese dall'allocatore e perché
    """
    folder_path = create_folder_with_timestamp(base_path=base_report_path)
    population_data_path = "data/rwa_pd_2020_1km_UNadj_ASCII_XYZ.csv"
    unconnected_school_extractor = SchoolsExtractor('data\school_geolocations_with-connnectivity.csv')
    data = unconnected_school_extractor.get_unconnected_schools(choosen_country)
    save_settings(choosen_country, budget, folder_path, "settings.json")

    unconnected_schools = data.head(50)  # sample of original dataset
    technology_extractor_config = read_json('config/technology_extractor_config.json')
    technology_extractor = TechnologyExtractor(technology_extractor_config)
    technology_extractor.initalize_disconnected_schools(unconnected_schools)
    data = technology_extractor.get_df_technologies_avaiable_for_disconnected_schools()
    technology_data_path = write_data_to_csv(data, folder_path, filename='unconnected_schools_technology.csv')
    system_prompt_estimator_llm = read_file("src\\prompt\\cost_estimator_system.txt")
    llm_estimator_cost = LLMEstimatorCost(system_prompt_estimator_llm, technology_data_path, folder_path, api_key)
    # Salva un JSON con informazione su stima dei costi per implemtazione tecnolgia in una scuola
    estimation_technlogy_path = llm_estimator_cost.save_response_to_file(choosen_country, model="mistralai/codestral-2501") 
    data_transformer = DataTransformer(choosen_country, population_data_path, estimation_technlogy_path)
    data_for_allocator = data_transformer.transform_data()
    resource_allocator = ResourceAllocator(data_for_allocator)
    results_allocator = resource_allocator.calculate_best_allocation(budget)
    write_file_txt(results_allocator, folder_path, 'resource_allocator_results.txt')
    system_prompt = read_file("src\\prompt\\document_creator.txt")
    document_generator = DocumentGenerator(allocator_data=results_allocator,
                                           system_prompt=system_prompt,
                                           folder_path=folder_path,
                                           api_key=api_key
                                           )
    markdown = document_generator.save_response_to_file(choosen_country, budget, model="mistralai/codestral-2501", return_response=True)
    return markdown
    
