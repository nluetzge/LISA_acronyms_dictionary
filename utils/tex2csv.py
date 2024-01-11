#!/usr/bin/env python
"""Script to create a list out of an acronym.tex file """
#########################################################################
# IDENT			tex2csv.py
# LANGUAGE		Python
# AUTHOR		N. Luetzgendorf
# PURPOSE       This is a script that takes the acronums.tex file
#               and creates a new table of acronyms. Its a bit of a hack but worked
#               This was used to take all the redbook acronyms back into the list
#
# usage: tex2csv.py [-h]
#
#
# optional arguments:
# -h, --help  show this help message and exit

# VERSION
# 1.0.0 13.05.2023 NL Creation
#
#########################################################################
# ===============================================================
# Imports
# ===============================================================
from astropy.table import Table
from pathlib import Path
import re

_table_dic = {'Acronym': 'U10',
              'Translation': 'U80',
              'Description': 'U300',
              }
# ===============================================================
# Input Parse
# ===============================================================
# Read the table of acronyms
filename = Path(__file__).resolve().parent / 'acronym.tex'

f=open(filename)
lines=f.readlines()

tb_tex = Table(names=_table_dic.keys(), dtype=_table_dic.values())

for li in lines:
    if li[:11]=='\\newacronym':
        content=re.split('{|}', li[11:])
        if len(content)==7:
            ac=content[3]
            descr=content[5]
        elif len(content)==9:
            if content[5]=='\\glspt':
                ac=content[3]
                descr=content[6].split('sci:')[1]
            else:
                ac=content[5]
                descr=content[7]
        elif len(content)==11:
            ac=content[3]
            descr=content[-3]
        elif len(content) in [13,15]:
            ac=content[5]
            descr=content[-3]
        else:
            print('Something is wrong')
            print(li)
        if ac=='\glslink':
            print('Something is wrong')
            print(li)
        print(ac, descr)
        tb_tex.add_row([ac, descr,''])

tb_tex.write('tables/LISA_acronyms_Redbooktex.csv', overwrite=True)