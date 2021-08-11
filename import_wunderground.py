import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt
import string
import helpful_functions as hf


# db_connection_string = 'sqlite:///Resources/energy_data.db'
wunderground_csv_path_prefix = 'Resources/WeatherUnderground/Houston/Houston_'
city_list = ['Austin', 'Corpus_Christi', 'Dallas', 'San_Angelo', 'San_Antonio']
year_list = ['2020', '2021']


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
    csv_path_dict = {}
    for year in year_list:
        csv_path_dict[year] = {}

    for city in city_list:
        for year in year_list:
            csv_path_list = []
            for i in range(1, 29):
                day_string = str(i).zfill(2)
                path_prefix = hf.gen_wu_csv_path(city)
                csv_path = Path(path_prefix + year + '_02_' + day_string + '.csv')
                csv_path_list.append(csv_path)
            csv_path_dict[year][city] = csv_path_list
    print(csv_path_dict)

    engine = sqlalchemy.create_engine(hf.db_connection_string)
    for city in city_list:
        for year in year_list:
            df = pd.read_csv(csv_path_dict[year][city][0])
            df['Datetime'] = df.apply(lambda x: gen_datetime(dt.date(2020,2,1), x['Time']),axis=1)
            df = clean_dataframe(df)
            for i, path in enumerate(csv_path_dict[year][city][1:]):
                new_df = pd.read_csv(path)
                new_df['Datetime'] = new_df.apply(lambda x: gen_datetime(dt.date(2020,2,i+2), x['Time']),axis=1)
                new_df = clean_dataframe(new_df)
                df = df.append(new_df, ignore_index=True)
            df.set_index('Datetime', inplace=True)
            print(df)
            table_name = 'WU_' + city + '_' + year
            df.to_sql(table_name, con=engine, if_exists='replace')



#    Feb 2020 filenames
    csv_path_list = []
    for i in range (1, 29):
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

#    Feb 2021 filenames
    csv_path_list = []
    for i in range (1, 29):
        day_string = str(i).zfill(2)
        csv_path = Path(wunderground_csv_path_prefix + '2021-02-' + day_string + '.csv')
        csv_path_list.append(csv_path)

    wu_2021_df = pd.read_csv(csv_path_list[0])
    wu_2021_df['Datetime'] = wu_2021_df.apply(lambda x: gen_datetime(dt.date(2021,2,1), x['Time']),axis=1)
    wu_2021_df = clean_dataframe(wu_2021_df)
    for i, path in enumerate(csv_path_list[1:]):
        new_df = pd.read_csv(path)
        new_df['Datetime'] = new_df.apply(lambda x: gen_datetime(dt.date(2021,2,i+2), x['Time']),axis=1)
        new_df = clean_dataframe(new_df)

        wu_2021_df = wu_2021_df.append(new_df, ignore_index=True)
    wu_2021_df.set_index('Datetime', inplace=True)
    print(wu_2021_df)

    wu_2020_df.to_sql('WU_Houston_2020', con=engine, if_exists='replace')
    wu_2021_df.to_sql('WU_Houston_2021', con=engine, if_exists='replace')
    inspector = sqlalchemy.inspect(engine)
    print(inspector.get_table_names())
    return


if __name__ == '__main__':
    print('Importing Weather Underground CSV files...')
    run()
