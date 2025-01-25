import pandas as pd


class UnconnectedSchoolsExtractor:
    def __init__(self, path):
        self.path = path
        self.data = self._load_data(self.path)

    def _load_data(self, path):
        data = pd.read_csv(path)
        return data
    
    def get_unconnected_schools(self, country=None):
        output_columns = ['country', 'education_level', 'school_name', 'latitude', 'longitude']
        if country is None:
            return self.data[self.data['connectivity'] == 'No'].reset_index(drop=True)\
                [output_columns]
        else:
            return self.data[(self.data['country'] == country) & (self.data['connectivity'] == 'No')].reset_index(drop=True)\
                [output_columns]
        