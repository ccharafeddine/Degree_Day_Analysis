import pandas as pd
from pathlib import Path
import sqlalchemy

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
year_list = ['2019', '2020', '2021']

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


def run():
    engine = sqlalchemy.create_engine(db_connection_string)
    ercot_rtm_2020 = get_ercot_year_df(rtm_path_prefix, '2020')
    ercot_rtm_2021 = get_ercot_year_df(rtm_path_prefix, '2021')
    
    ercot_rtm_2020.to_sql('ERCOT_2020', engine)
    ercot_rtm_2020.to_sql('ERCOT_2021', engine)
        
if __name__ == '__main__':
    print('Importing CSV files...')
    run()