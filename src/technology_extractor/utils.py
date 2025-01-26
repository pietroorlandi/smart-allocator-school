import math
import numpy as np
import pandas as pd


def get_offset_in_degrees(latitude: float, distance_km: float = 1.0) -> tuple[float, float]:
    """
    Ritorna l'offset di latitudine e longitudine per una distanza di 'distance_km' -> (lat_offset, lon_offset)
    """
    # Un grado di latitudine corrisponde a circa 111 km
    lat_offset = distance_km / 111.0
    
    # A latitudini più alte, la distanza per grado di longitudine cambia
    lon_offset = distance_km / (111.0 * math.cos(math.radians(latitude)))
    
    return lat_offset, lon_offset


def haversine(lat1, lon1, lat2, lon2):
        R = 6371.0  # Raggio della Terra in km
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance


def haversine_vectorized(lat1: pd.Series, lon1: pd.Series, lat2: float, lon2: float):
    # Converti in radianti
    lat1_rad, lon1_rad = np.radians(lat1), np.radians(lon1)
    lat2_rad, lon2_rad = np.radians(lat2), np.radians(lon2)

    # Calcolo della distanza Haversine
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = np.sin(dlat / 2)**2 + np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    # Raggio terrestre in km
    R = 6371.0
    return R * c