# IDENT			code.py
# LANGUAGE		Python
# AUTHOR		N. LUETZGENDORF
# PURPOSE		
#
# VERSION
# 1.0.0 DD.MM.YYYY NL Creation
# ===============================================================
# Imports
# ===============================================================
from acronym_gui import read_acronyms
import pandas as pd
import sqlite3

filename = 'tables/LISA_acronyms.csv'
tb_all = read_acronyms(filename)

df = tb_all.to_pandas()

conn = sqlite3.connect('acronyms.db')

df.to_sql('Acronyms', conn, if_exists='replace', index=False)
conn.commit()
conn.close()