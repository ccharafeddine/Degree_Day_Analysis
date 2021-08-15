import os
from dotenv import load_dotenv
from pathlib import Path
import pandas as pd
import plotly.express as px

db_connection_string = 'sqlite:///Resources/energy_data.db'

year_list = ['2020', '2021']
city_list = ['Austin', 'Corpus_Christi', 'Dallas', 'San_Angelo', 'San_Antonio']
city_list_2 = ['Austin', 'Corpus_Christi', 'Dallas', 'Houston', 'San_Angelo', 'San_Antonio']
cities = ['Austin', 'Corpus_Christi', 'Dallas', 'Houston', 'San_Angelo', 'San_Antonio']
data_sources = ['DegreeDays', 'WU', 'ERCOT']

dti_dict = {
    '2020' : pd.DataFrame(pd.date_range(
        "2020-02-01", 
        periods=24*28*4, 
        freq="15T", 
        name='Datetime')
                         ),
    '2021' : pd.DataFrame(pd.date_range(
        "2021-02-01", 
        periods=24*28*4, 
        freq="15T", 
        name='Datetime')
                         )
}
dd_df_dict = {}


def get_mapbox_api_token():
    # Load the .env file into the notebook
    load_dotenv()

    # Read in your MAPBOX_API_KEY
    mapbox_api_access_token = os.getenv("MAPBOX_API_ACCESS_TOKEN")

    # Confirm the availability of your Mapbox API access token by checking its type
    if type(mapbox_api_access_token) == type(''):
    # Set your Mapbox API access token
        px.set_mapbox_access_token(mapbox_api_access_token)
        print('Mapbox API verified.')
        return mapbox_api_access_token
    else:
        print('Error loading Mapbox API Token. Check your .env file.')
        return None


def gen_wu_csv_path(city_name):
    csv_path = 'Resources/WeatherUnderground/' + city_name + '/' + city_name + '_'
    return csv_path

def gen_wu_csv_dict():
    csv_path_dict = {}
    for year in year_list:
        csv_path_dict[year] = {}

    for city in city_list:
        for year in year_list:
            csv_path_list = []
            for i in range(1, 29):
                day_string = str(i).zfill(2)
                path_prefix = gen_wu_csv_path(city)
                csv_path = Path(path_prefix + year + '_02_' + day_string + '.csv')
                csv_path_list.append(csv_path)
            csv_path_dict[year][city] = csv_path_list
    return csv_path_dict
