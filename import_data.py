import pandas as pd
from pathlib import Path
import sqlalchemy

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
year_list = ['2019', '2020', '2021']
interval_minutes = [0, 15, 30, 45]

db_connection_string = 'sqlite:///Resources/energy_data.db'

dam_path_prefix = 'Resources/ERCOT/rpt.00013060.0000000000000000.DAMLZHBSPP_'
rtm_path_prefix = 'Resources/ERCOT/rpt.00013061.0000000000000000.RTMLZHBSPP_'


def get_ercot_year_df(path_prefix, year_str):
    csv_path = Path(path_prefix + year_str + '.xlsx')
    df = pd.read_excel(csv_path, sheet_name=month_list[1])
#    for month in month_list[1:2]:
#        temp_df = pd.read_excel(csv_path, sheet_name=month)
#        df = pd.concat([df, temp_df], ignore_index=True)
    return df


def clean_rtm_data(df):
    filter_column = 'Settlement Point Name'
    settlement_point_filter = 'HB_HOUSTON'
    df = filter_rtm_data(df, filter_column, settlement_point_filter)
    df = append_datetime_column(df)
    df = arrange_ercot_columns(df)
    return df


def filter_rtm_data(df, filter_column, filter_value):
    settlement_point_filter = 'HB_HOUSTON'
    df = df.loc[ercot_rtm_df[filter_column] == filter_value]
    df.reset_index(drop=True, inplace=True)
    return df


def append_datetime_column(df):
    new_column = []
    for i in df.index:
        print(f'\r{100*i/df.index.stop:5.1f}% complete... ', end='')
#         new_column.append(create_datetime(df, i))
        new_column.append(create_datetime(df[i]['Delivery Date'], df[i]['Delivery Hour'], df[i]['Delivery Interval']))
    print('Done.')
    df['Datetime'] = new_column
    return df


def create_datetime(date_string, hour_int, interval_index):
    format_str = '%m/%d/%Y' # The format
    datetime_obj = dt.datetime.strptime(date_string, format_str)
    time_delta = dt.timedelta(hours=hour_int, minutes=interval_minutes[interval_index-1])
    date_time = datetime_obj + time_delta
    return date_time


def arrange_ercot_columns(df):
    drop_columns_list = ['Delivery Date', 'Delivery Hour', 'Delivery Interval', 'Repeated Hour Flag', 'Settlement Point Name', 'Settlement Point Type']
    df.drop(columns=drop_columns_list, inplace=True)
    df = df[['Datetime', 'Settlement Point Price']]
    df.set_index('Datetime', inplace=True)
    return df


def run():
    engine = sqlalchemy.create_engine(db_connection_string)
    ercot_rtm_2020 = get_ercot_year_df(rtm_path_prefix, '2020')
    ercot_rtm_2021 = get_ercot_year_df(rtm_path_prefix, '2021')
    
    ercot_rtm_2020 = clean_rtm_data(ercot_rtm_2020)
    ercot_rtm_2021 = clean_rtm_data(ercot_rtm_2021)
    
    ercot_rtm_2020.to_sql('ERCOT_2020', engine)
    ercot_rtm_2021.to_sql('ERCOT_2021', engine)

    
if __name__ == '__main__':
    print('Importing CSV files...')
    run()