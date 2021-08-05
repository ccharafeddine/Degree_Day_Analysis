import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt


wunderground_csv_path_prefix = 'Resources/WeatherUnderground/Houston/Houston_'


def run():
    # Feb 2020 filenames
    csv_path_list = []
    for i in range (1, 30):
        day_string = str(i).zfill(2)
        csv_path = Path(wunderground_csv_path_prefix + '2020-02-' + day_string + '.csv')
        csv_path_list.append(csv_path)
    # print(csv_path_list)
    wu_2020_df = pd.read_csv(csv_path_list[0])
    print(wu_2020_df)

if __name__ == '__main__':
    print('Importing Weather Underground CSV files...')
    run()