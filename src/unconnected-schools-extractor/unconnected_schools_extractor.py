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
        
# if __name__ == '__main__':
#     unconnected_school_extractor = UnconnectedSchoolsExtractor('data\school_geolocations_with-connnectivity.csv')
#     data = unconnected_school_extractor.get_unconnected_schools('Rwanda')
#     print(data)
#     mask = data['education_level'] == 'Primary'
#     print(sum(mask))