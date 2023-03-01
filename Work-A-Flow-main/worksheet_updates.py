import pandas as pd
import sqlite3

def updates():
    db = sqlite3.connect('CHRS.db')
    data = pd.read_sql_query("select * from worksheet", db)
    