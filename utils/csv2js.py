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
from acronym_gui import read_acronyms
import numpy.ma as ma
import json
from datetime import datetime
import time

_table_dic = {'Acronym': 'U10',
              'Translation': 'U80',
              'Description': 'U300',
              }
# ===============================================================
# Input Parse
# ===============================================================
# Read the table of acronyms
filename = 'tables/LISA_acronyms.csv'
tb_all = read_acronyms(filename)

# ===============================================================
# Writing
# ===============================================================
result = {}
for tb in tb_all:
    if tb['Acronym'] not in result:
        if ma.is_masked(tb['Description']):
            result[tb['Acronym']] = {'Translation':tb['Translation']}
        else:
            result[tb['Acronym']] = {'Translation':tb['Translation'] , 'Description':tb['Description']}
    else:
        print('{} is double'.format(tb['Acronym']))
        if ma.is_masked(tb['Description']):
            result[tb['Acronym']]['Translation2'] = tb['Translation']
        else:
            result[tb['Acronym']]['Translation2'] = tb['Translation']
            result[tb['Acronym']]['Description2'] = tb['Description']

t0 = time.time()
with open("LISADict.js", "w") as outfile:
    outfile.write('// Created on {}\n'.format(datetime.fromtimestamp(t0).strftime("%Y%m%dT%H%M")))
    outfile.write('LISADict=')
    json.dump(result, outfile, indent=4)
