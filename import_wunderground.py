import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt
import string


wunderground_csv_path_prefix = 'Resources/WeatherUnderground/Houston/Houston_'

def gen_datetime(date_obj, time_str):
    time_obj = dt.datetime.strptime(time_str, '%I:%M %p')
    time_delta = dt.timedelta(hours=time_obj.hour, minutes=time_obj.minute)
    datetime_obj = dt.datetime(date_obj.year, date_obj.month, date_obj.day) + time_delta
    return datetime_obj

def clean_dataframe(df):
    drop_columns = ['Time', 'Dew Point', 'Humidity', 'Wind', 'Wind Speed', 'Wind Gust', 'Pressure', 'Precip.', 'Condition']
    df.drop(columns=drop_columns, inplace=True)
    df = df[['Datetime', 'Temperature']]
    df['Temperature'] = df.apply(lambda x: strip_non_printable(x['Temperature']), axis=1)
    return df


def strip_non_printable(my_str):
    return int(''.join([x for x in my_str if x in string.printable])[:-1])


def run():
    # Feb 2020 filenames
    csv_path_list = []
    for i in range (1, 30):
        day_string = str(i).zfill(2)
        csv_path = Path(wunderground_csv_path_prefix + '2020-02-' + day_string + '.csv')
        csv_path_list.append(csv_path)

    wu_2020_df = pd.read_csv(csv_path_list[0])
    wu_2020_df['Datetime'] = wu_2020_df.apply(lambda x: gen_datetime(dt.date(2020,2,1), x['Time']),axis=1)
    wu_2020_df = clean_dataframe(wu_2020_df)
    for i, path in enumerate(csv_path_list[1:]):
        new_df = pd.read_csv(path)
        new_df['Datetime'] = new_df.apply(lambda x: gen_datetime(dt.date(2020,2,i+2), x['Time']),axis=1)
        new_df = clean_dataframe(new_df)

        wu_2020_df = wu_2020_df.append(new_df, ignore_index=True)
    wu_2020_df.set_index('Datetime', inplace=True)
    print(wu_2020_df)


if __name__ == '__main__':
    print('Importing Weather Underground CSV files...')
    run()