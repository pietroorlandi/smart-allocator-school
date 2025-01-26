import pandas as pd
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'src')))
from utils.utils import get_offset_in_degrees, haversine_vectorized
from schools_extractor.schools_extractor import SchoolsExtractor

config = json.load(open('config/connected_schools_extr_config.json'))


class IsolationIndexCalculator:
    def __init__(self, country: str = 'Rwanda'):
        schools_extractor = SchoolsExtractor(config.get('schools_connection_dataset_path'))
        self.connected_schools = schools_extractor.get_connected_schools(country=country)
        self.unconnected_schools = schools_extractor.get_unconnected_schools(country=country)

    def compute_nearby_connected_schools(self, tolerance: float = 10.0) -> pd.DataFrame:
        """ 
        Compute the number and distance of connected schools within a given distance tolerance for each unconnected school. Default tolerance is 10 km.
        Returns a DataFrame with the isolation index and list of distances for each unconnected school.
        """
        
        # Initialize lists to store results
        count_connected_schools = []
        distances_list = []

        # Iterate over each unconnected school
        for _, unconnected_school in self.unconnected_schools.iterrows():
            latitude = unconnected_school['latitude']
            longitude = unconnected_school['longitude']
            lat_offset, lon_offset = get_offset_in_degrees(latitude, tolerance)

            # Define bounding box
            lat_min = latitude - lat_offset
            lat_max = latitude + lat_offset
            lon_min = longitude - lon_offset
            lon_max = longitude + lon_offset

            # Filter connected schools within the bounding box
            mask_bool = (
                (self.connected_schools['latitude'] >= lat_min) & 
                (self.connected_schools['latitude'] <= lat_max) & 
                (self.connected_schools['longitude'] >= lon_min) & 
                (self.connected_schools['longitude'] <= lon_max)
            )
            filtered_data = self.connected_schools[mask_bool]

            # Calculate distances for filtered connected schools
            distances = haversine_vectorized(
                filtered_data['latitude'], 
                filtered_data['longitude'], 
                latitude, 
                longitude
            )

            # Filter schools truly within the tolerance radius
            within_radius = distances <= tolerance
            nearby_schools = filtered_data[within_radius]

            # Add the count of nearby schools and list of distances for the current unconnected school
            count_connected_schools.append(len(nearby_schools))
            distances_list.append(distances[within_radius].tolist())

        # Add the new columns to the original unconnected_schools DataFrame
        self.unconnected_schools['isolation_index'] = count_connected_schools
        self.unconnected_schools['connected_schools_distances'] = distances_list

        return self.unconnected_schools
