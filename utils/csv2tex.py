#!/usr/bin/env python
"""Script to create an acronym.tex file out of the list"""
#########################################################################
# IDENT			csv2tex.py
# LANGUAGE		Python
# AUTHOR		N. Luetzgendorf
# PURPOSE       This is a script that creates an acronym.tex file
#               for the acronyms usepackage in latex from the csv acronym table.
#
# usage: csv2tex.py [-h]
#
#
# optional arguments:
# -h, --help  show this help message and exit

# VERSION
# 1.0.0 13.01.2023 NL Creation
# 1.0.1 27.10.2023 NL Update renamed tex_acronym.py
#########################################################################
# ===============================================================
# Imports
# ===============================================================
import time
from datetime import datetime
from astropy.table import unique
from pathlib import Path
from acronym_gui import read_acronyms

_table_dic = {'Acronym': 'U10',
              'Translation': 'U80',
              'Description': 'U300',
              }
# ===============================================================
# Input Parse
# ===============================================================
# Read the table of acronyms
filename = Path(__file__).resolve().parent / 'tables/LISA_acronyms.csv'
tb_all = read_acronyms(filename)

# Make sure we have just one for each:
tb_uni = unique(tb_all, keys='Acronym')

t0 = time.time()
t0_string = datetime.fromtimestamp(t0).strftime("%d/%m/%Y (%H:%M)")
with open('acronym.tex', 'w') as f:
    f.write('% Automatically created with tex_acronyms.py (https://github.com/nluetzge/LISA_acronyms_dictionary/tex_acronyms.py) \n')
    f.write('% Date: {:}\n'.format(t0_string))
    f.write('% Currently we have {:} acronyms on file \n'.format(len(tb_uni)))
    f.write('% \n')
    f.write('% \n')
    for tab in tb_uni:
        f.write('\\newacronym{'+tab['Acronym']+'}{'+tab['Acronym']+'}{'+tab['Translation']+'}\n')
