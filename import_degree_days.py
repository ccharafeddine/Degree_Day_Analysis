import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt

db_connection_string = 'sqlite:///Resources/energy_data.db'
csv_path = Path('Resources/DegreeDays/KHOU_HDD_65F.csv')

austin_csv_path = Path('Resources/DegreeDays/KAUS_HDD_65F.csv')
corpus_christi_csv_path = Path('Resources/DegreeDays/KCRP_HDD_65F.csv')
dallas_csv_path = Path('Resources/DegreeDays/KDAL_HDD_65F.csv')
houston_csv_path = Path('Resources/DegreeDays/KHOU_HDD_65F.csv')
san_angelo_csv_path = Path('Resources/DegreeDays/KSJT_HDD_65F.csv')
san_antonio_csv_path = Path('Resources/DegreeDays/KSAT_HDD_65F.csv')


def convert_datestring_to_datetime(date_str):
    datetime_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    return datetime_obj


dd_df = pd.read_csv(csv_path, skiprows=6)
dd_df.drop(columns=['% Estimated'], inplace=True)
dd_df['Date'] = dd_df.apply(lambda x: convert_datestring_to_datetime(x['Date']), axis=1)
dd_df.set_index('Date', inplace=True)
print(dd_df)
start_date_2020 = dt.datetime(2020,2,1)
end_date_2020 = dt.datetime(2020,2,29)
dd_2020_df = dd_df.loc[start_date_2020: end_date_2020]
print(dd_2020_df)
start_date_2021 = dt.datetime(2021,2,1)
end_date_2021 = dt.datetime(2021,2,28)
dd_2021_df = dd_df.loc[start_date_2021: end_date_2021]
print(dd_2021_df)

engine = sqlalchemy.create_engine(db_connection_string)
dd_2020_df.to_sql('DegreeDays_2020', con=engine, if_exists='replace')
dd_2021_df.to_sql('DegreeDays_2021', con=engine, if_exists='replace')

inspector = sqlalchemy.inspect(engine)
print(inspector.get_table_names())