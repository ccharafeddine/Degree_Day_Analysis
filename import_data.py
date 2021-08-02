import pandas as pd
from pathlib import Path

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
year_list = ['2019', '2020', '2021']

dam_path_prefix = 'Resources/ERCOT/rpt.00013060.0000000000000000.DAMLZHBSPP_'
rtm_path_prefix = 'Resources/ERCOT/rpt.00013061.0000000000000000.RTMLZHBSPP_'

def get_ercot_year_df(path_prefix, year_str):
    csv_path = Path(path_prefix + year_str + '.xlsx')
    df = pd.read_excel(csv_path, sheet_name=month_list[0])
    for month in month_list[1:]:
        temp_df = pd.read_excel(csv_path, sheet_name=month)
        df = pd.concat([df, temp_df], ignore_index=True)
    return df


def run():
    print(f'Importing ERCOT {year_list[0]} data from CSV into DataFrame...', end='')
    ercot_df = get_ercot_year_df(rtm_path_prefix, year_list[0])
    print('Done!')
    print(ercot_df.head())
    for year in year_list[1:]:
        print(f'Importing ERCOT {year} data from CSV into DataFrame...', end='')
        new_df = get_ercot_year_df(rtm_path_prefix, year)
        print('Done!')
        print(new_df.head())
        ercot_df = pd.concat([ercot_df, new_df], ignore_index=True,)
    print(ercot_df.head())
    print(ercot_df.tail())
        
if __name__ == '__main__':
    print('Importing CSV files...')
    run()