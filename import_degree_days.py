import pandas as pd
from pathlib import Path
import sqlalchemy
import datetime as dt

db_connection_string = 'sqlite:///Resources/energy_data.db'
csv_path = Path('Resources/DegreeDays/KHOU_HDD_65F.csv')

dd_df = pd.read_csv(csv_path)
print(dd_df)