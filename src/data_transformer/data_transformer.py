import pandas as pd
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from isolation_index_calculator.isolation_index_calculator import IsolationIndexCalculator
from density_population_extractor.density_population_extractor import DensityExtractor
from technology_extractor.technology_extractor import read_json

class DataTransformer:
    def __init__(self,
                selected_country: str,
                population_data_path: str,
                estimation_technlogy_path: str):
        self.population_data_path = population_data_path
        self.selected_country = selected_country
        self.estimation_technology_path = estimation_technlogy_path

    def transform_data(self):
        isolation_index_calculator = IsolationIndexCalculator(country='Rwanda')
        isolation_index_calculator.compute_nearby_connected_schools(tolerance=10.0)
        unconnected_schools = isolation_index_calculator.unconnected_schools
        unconnected_schools = unconnected_schools.head(50)
        estimation_technology_data = read_json(self.estimation_technology_path)
        density_population_extractor = DensityExtractor(self.population_data_path)
        density_population_extractor.load_csv_data()
        isolation_index_calculator.compute_nearby_connected_schools(tolerance=10.0)
        population_density_list = []

        # Associate the population density to each unconnected school
        for unconnected_school in unconnected_schools.iterrows():
            latitude = unconnected_school[1]['latitude']
            longitude = unconnected_school[1]['longitude']
            
            density = density_population_extractor.get_min_distance_density(latitude=latitude, longitude=longitude)
            population_density_list.append(density)
        unconnected_schools['population_density'] = population_density_list

        data_structure_allocator = []
        for estimated_cost in estimation_technology_data:
            data_allocator = {}
            id_school = estimated_cost['id_school']
            mask_bool = unconnected_schools['school_id_giga'] == id_school
            unconnected_school = unconnected_schools[mask_bool]
            try:
                isolation_index = unconnected_school['isolation_index'].values[0]
                population_density = unconnected_school['population_density'].values[0]
                estimated_cost_broadband = estimated_cost["estimation_cost_broadband"] if estimated_cost["estimation_cost_broadband"] != -1 else 500000
                estimation_cost_cellular_tower = estimated_cost["estimation_cost_cellular_tower"] if estimated_cost["estimation_cost_cellular_tower"] != -1 else 500000
                data_allocator['school_id'] = id_school
                data_allocator['pop_density'] = population_density
                data_allocator['isolation'] = isolation_index
                data_allocator['costs'] = [estimated_cost_broadband, estimation_cost_cellular_tower]
                data_allocator['reason'] = [estimated_cost["reason_broadband"], estimated_cost["reason_cellular_tower"]]
                data_structure_allocator.append(data_allocator)
            except Exception:
                pass
            
        return data_structure_allocator
        
        
# if __name__ == '__main__':
#     selected_country = "Rwanda"
#     population_data_path = "data/input/DensityData/rwa_pd_2020_1km_UNadj_ASCII_XYZ.csv"
#     estimation_technlogy_path = 'report/2025-01-26_14-56-29/estimation_cost.json'
#     data_transformer = DataTransformer(selected_country, population_data_path, estimation_technlogy_path)
#     data_for_allocator = data_transformer.transform_data()

