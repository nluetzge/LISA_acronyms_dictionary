#!/usr/bin/env python
"""Script to merge two acronym tables"""
#########################################################################
# IDENT			merge_tables.py
# LANGUAGE		Python
# AUTHOR		N. Luetzgendorf
# PURPOSE       This is a gui to search for LISA acronyms
#				It uses Tkinter and a csv file with the acronyms
#				to search and provide a translation to acronyms related
#				to LISA (Laser Interferometer Space Antenna).
#
# usage: merge_tables.py [-h] table
#
# positional arguments:
# table       Filename of the new acronym table that you want to merge
#
# optional arguments:
# -h, --help  show this help message and exit

# VERSION
# 1.0.0 08.09.2021 NL Creation
#
#########################################################################
# ===============================================================
# Imports
# ===============================================================
import os
import time
from datetime import datetime
import numpy as np
from astropy.table import join, Table, unique
from pathlib import Path
from acronym_gui import read_acronyms
import argparse

_table_dic = {'Acronym': 'U10',
              'Translation': 'U80',
              'Description': 'U300',
              }
# ===============================================================
# Input Parse
# ===============================================================
parser = argparse.ArgumentParser()
# Help
arghelp = 'Filename of the new acronym table that you want to merge'

# Args
parser.add_argument('table', type=str, help=arghelp)

# Parse parameters
args = parser.parse_args()
table_filename = args.table

# Read the table of acronyms
filename = Path(__file__).resolve().parent / 'tables/LISA_acronyms.csv'
tb_all = read_acronyms(filename)
tb_add = read_acronyms(table_filename)
if tb_add.colnames[0]=='\ufeffAcronym':
    tb_add.rename_column('\ufeffAcronym', 'Acronym')


tb_new = join(tb_all, tb_add, keys='Acronym', join_type='outer')

# Create a new master table
tb_out = Table([np.char.upper(tb_new['Acronym'].data),
                tb_new['Translation_1'].data,
                tb_new['Description_1'].data], names=_table_dic.keys(), dtype=_table_dic.values())


# Fill in the blanks from the previous master table with the new table
tb_out['Translation'][tb_new['Translation_1'].mask] = tb_new['Translation_2'][tb_new['Translation_1'].mask]
tb_out['Description'][tb_new['Description_1'].mask] = tb_new['Description_2'][tb_new['Description_1'].mask]

# Find duplicates that are different from what we already have
find = ((tb_new['Translation_1'].mask==False) & (tb_new['Translation_2'].mask==False)) &\
       (tb_new['Translation_1'] != tb_new['Translation_2'])
if find.any():
    tb_tmp = tb_new[find]
    for tb in tb_tmp:
        tb_out.add_row([tb['Acronym'],tb['Translation_2'],tb['Description_2']])


# Remove duplicates (just in case)
n_before = len(tb_out)
tb_out = unique(tb_out, keys=['Acronym', 'Translation'], keep='first')
n_after = len(tb_out)
print('Removed {:} duplicates'.format(n_before-n_after))

# How many acronyms did we add?
nadd = len(tb_out) - len(tb_all)
print('Added {:d} new acronyms'.format(nadd))
i=0
for t in tb_out:
    if t['Acronym'] not in tb_all['Acronym']:
        print(i, t['Acronym'])
        i+=1
# ===============================================================
# Writing
# ===============================================================
t0 = time.time()
t0_string = datetime.fromtimestamp(t0).strftime("%Y%m%dT%H%M")
base_filename = str.split(str(filename), '.csv')[0]

# Copying the previoys master file to a backup file
os.system('mv {:s}.csv {:s}_{:s}.csv'.format(base_filename, base_filename, t0_string))

# Writing out the new master file
print('Writing {:s}'.format(str(filename)))
tb_out.write(filename)