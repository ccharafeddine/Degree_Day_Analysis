import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt
import helpful_functions as hf


csv_path_dict = {
    'Austin': Path('Resources/DegreeDays/KAUS_HDD_65F.csv'),
    'Corpus_Christi': Path('Resources/DegreeDays/KCRP_HDD_65F.csv'),
    'Dallas': Path('Resources/DegreeDays/KDAL_HDD_65F.csv'),
    'Houston': Path('Resources/DegreeDays/KHOU_HDD_65F.csv'),
    'San_Angelo': Path('Resources/DegreeDays/KSJT_HDD_65F.csv'),
    'San_Antonio': Path('Resources/DegreeDays/KSAT_HDD_65F.csv'),
}


def convert_datestring_to_datetime(date_str):
    datetime_obj = dt.datetime.strptime(date_str, '%Y-%m-%d')
    return datetime_obj


def gen_df_from_path_and_date_range(csv_path, start_date, end_date):
    print(csv_path, start_date, end_date)
    dd_df = pd.read_csv(csv_path, skiprows=6)
    print(dd_df.head())
    dd_df.drop(columns=['% Estimated'], inplace=True)
    dd_df['Date'] = dd_df.apply(lambda x: convert_datestring_to_datetime(x['Date']), axis=1)
    dd_df.set_index('Date', inplace=True)
    return dd_df.loc[start_date: end_date]


def gen_db_tables():
    engine = sqlalchemy.create_engine(hf.db_connection_string)

    for year in hf.year_list:
        for city in hf.city_list_2:
            start_date = dt.datetime(int(year),2,1)
            end_date = dt.datetime(int(year),2,28)
            print(city, year, start_date, end_date)
            df = gen_df_from_path_and_date_range(csv_path_dict[city], start_date, end_date)
            print(df)
            df.to_sql('DegreeDays_'+city+'_'+year, con=engine, if_exists='replace')
    inspector = sqlalchemy.inspect(engine)
    print(inspector.get_table_names())
    return


if __name__ == '__main__':
    print("Generating db tables")
    gen_db_tables()
