import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt
import helpful_functions

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
year_list = ['2019', '2020', '2021']
interval_minutes = [0, 15, 30, 45]

db_connection_string = 'sqlite:///Resources/energy_data.db'
rtm_csv_path_prefix = 'Resources/ERCOT/RTM-'

def get_ercot_year_df(path_prefix, year_str):
    csv_path = Path(path_prefix + year_str + '.xlsx')
    df = pd.read_excel(csv_path, sheet_name=month_list[1])
    return df


def get_ercot_month_df(path_prefix, month_str):
    print(f'Getting data from csv: {month_str}')
    return pd.read_csv(Path(path_prefix + month_str + '.csv'))


def clean_rtm_data(df):
    filter_column = 'Settlement Point Name'
    settlement_point_filter = 'HB_HOUSTON'

    print(f"filtering data...")
    df = filter_rtm_data(df, filter_column, settlement_point_filter)

    print(f"appending datetime column...")
    df = append_datetime_column(df)

    print(f"arranging columns...")
    df = arrange_ercot_columns(df)
    
    print(f"removing commas...")
    df = remove_commas(df)

    print(f"done.")

    return df


def remove_commas(df):
    df['Settlement Point Price'] = df['Settlement Point Price'].replace(',', '', regex=True).astype('float')
    return df

def filter_rtm_data(df, filter_column, filter_value):
    df = df.loc[df[filter_column] == filter_value]
    df.reset_index(drop=True, inplace=True)
    return df


def append_datetime_column(df):
    new_column = []
    for i in df.index:
        print(f'\r{100*i/df.index.stop:5.1f}% complete... ', end='')
        # new_column.append(create_datetime(df[i]['Delivery Date'], df[i]['Delivery Hour'], df[i]['Delivery Interval']))
        new_column.append(create_datetime(df['Delivery Date'][i], df['Delivery Hour'][i], df['Delivery Interval'][i]))
    print('Done.')
#    df['Datetime'] = new_column
    df.loc[:, 'Datetime'] = new_column
    print(df.head())
    return df


def create_datetime(date_string, hour_int, interval_index):
    format_str = '%m/%d/%Y' # The format
    datetime_obj = dt.datetime.strptime(date_string, format_str)
    time_delta = dt.timedelta(hours=int(hour_int), minutes=interval_minutes[interval_index-1])
    date_time = datetime_obj + time_delta
    return date_time


def arrange_ercot_columns(df):
    print('arranging columns')
    drop_columns_list = ['Delivery Date', 'Delivery Hour', 'Delivery Interval', 'Repeated Hour Flag', 'Settlement Point Name', 'Settlement Point Type']
    df.drop(columns=drop_columns_list, inplace=True)
    df = df.loc[:, ('Datetime', 'Settlement Point Price')]
    df.set_index('Datetime', inplace=True)
    print('columns arranged')
    print(df.head())
    return df


def run():
    # ERCOT data
    engine = sqlalchemy.create_engine(db_connection_string)
    ercot_rtm_2020 = get_ercot_month_df(rtm_csv_path_prefix, '2020-02')
    ercot_rtm_2021 = get_ercot_month_df(rtm_csv_path_prefix, '2021-02')
    ercot_rtm_2020 = clean_rtm_data(ercot_rtm_2020)
    ercot_rtm_2021 = clean_rtm_data(ercot_rtm_2021)
    ercot_rtm_2020.to_sql('ERCOT_2020', engine, if_exists='replace')
    ercot_rtm_2021.to_sql('ERCOT_2021', engine, if_exists='replace')
    
    
if __name__ == '__main__':
    print('Importing CSV files...')
    run()