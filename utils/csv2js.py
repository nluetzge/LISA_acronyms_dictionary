#!/usr/bin/env python
"""Script to turn csv table into js datafile for the webtool"""
#########################################################################
# IDENT			csv2js.py
# LANGUAGE		Python
# AUTHOR		N. Luetzgendorf
# PURPOSE       Reads in the table and writes out a json-like file
#               that can be directly read into a JavaScript code
#
# usage: csv2js.py [-h]
#
# positional arguments:
#
# optional arguments:
# -h, --help  show this help message and exit

# VERSION
# 1.0.0 10.01.2024 NL Creation
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

def csv2js(inputtable):
    # ===============================================================
    # Writing
    # ===============================================================
    result = {}
    for tb in inputtable:
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

    return

if __name__ == '__main__':
    # ===============================================================
    # Input Parse
    # ===============================================================
    # Read the table of acronyms
    filename = 'tables/LISA_acronyms.csv'
    tb_all = read_acronyms(filename)
    csv2js(tb_all)