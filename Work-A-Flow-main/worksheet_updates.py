import pandas as pd
import sqlite3
def updates():
    db = sqlite3.connect('CHRS.db')
    data = pd.read_sql_query("select * from worksheet", db)
    data['HRA'] , data['Bonus2'], data['Con'] = 0, 0, 0
    data['Total'] = data['HRA'] + data['Bonus2'] + data['Con'] + data['Basic1']+ data['Special_Allowance1']+ data['CCA1']
    data.to_sql('worksheet',con = db,if_exists='replace')