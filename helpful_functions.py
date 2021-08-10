from pathlib import Path

db_connection_string = 'sqlite:///Resources/energy_data.db'

year_list = ['2020', '2021']
city_list = ['Austin', 'Corpus_Christi', 'Dallas', 'San_Angelo', 'San_Antonio']
city_list_2 = ['Austin', 'Corpus_Christi', 'Dallas', 'Houston', 'San_Angelo', 'San_Antonio']

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
