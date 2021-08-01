import pandas as pd
from pathlib import Path

month_list = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
year_list = ['2019', '2020', '2021']

dam_path_prefix = 'Resources/ERCOT/rpt.00013060.0000000000000000.DAMLZHBSPP_'
rtm_path_prefix = 'Resources/ERCOT/rpt.00013061.0000000000000000.RTMLZHBSPP_'

ercot_dam_2021_df = pd.read_excel(Path(dam_path_prefix + '2021.xlsx'), sheet_name=month_list[0])
for month in month_list[1:]:
    temp_df = pd.read_excel(Path(dam_path_prefix + '2021.xlsx'), sheet_name=month)
    ercot_dam_2021_df = pd.concat([ercot_dam_2021_df, temp_df], ignore_index=True)

ercot_dam_2020_df = pd.read_excel(Path(dam_path_prefix + '2020.xlsx'), sheet_name=month_list[0])
for month in month_list[1:]:
    temp_df = pd.read_excel(Path(dam_path_prefix + '2020.xlsx'), sheet_name=month)
    ercot_dam_2020_df = pd.concat([ercot_dam_2020_df, temp_df], ignore_index=True)

ercot_dam_2019_df = pd.read_excel(Path(dam_path_prefix + '2019.xlsx'), sheet_name=month_list[0])
for month in month_list[1:]:
    temp_df = pd.read_excel(Path(dam_path_prefix + '2019.xlsx'), sheet_name=month)
    ercot_dam_2019_df = pd.concat([ercot_dam_2019_df, temp_df], ignore_index=True)

ercot_dam_df = pd.concat([ercot_dam_2019_df, ercot_dam_2020_df, ercot_dam_2021_df], ignore_index=True)

print(ercot_dam_df.head(10))
print(ercot_dam_df.tail(10))


# ercot_rtm_2021_df = pd.read_excel(Path(rtm_path_prefix + '2021.xlsx'))

# ercot_rtm_2020_df = pd.read_excel(Path(rtm_path_prefix + '2020.xlsx'))

# ercot_rtm_2019_df = pd.read_excel(Path(rtm_path_prefix + '2019.xlsx'))

