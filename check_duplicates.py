# IDENT			check_duplicates.py
# LANGUAGE		Python
# AUTHOR		N. LUETZGENDORF
# PURPOSE		Little helper program to go check the duplicates and sort the table
#
# VERSION
# 1.0.0 DD.MM.YYYY NL Creation
# ===============================================================
# Imports
# ===============================================================
from acronym_gui import read_acronyms
from pathlib import Path
import numpy as np

# If you want to save the sorted table
safe = True

# Read the table of acronyms
filename = Path(__file__).resolve().parent / 'tables/LISA_acronyms.csv'
tb_all = read_acronyms(filename)
tb_all.sort('Acronym')

groups = tb_all.group_by('Acronym')


duplicate_indices = [list(np.arange(len(group))+index) for group, index in zip(groups.groups,
                                                                                groups.groups.indices) if len(group) > 1]

# This prints all the duplicates and you can check if its a "real" duplicate
for i, indices in enumerate(duplicate_indices):
    for idx in indices:
        print(i, groups[idx]['Acronym'], groups[idx]['Translation'])


if safe:
    # Writing out the new master file
    print('Writing {:s}'.format(str(filename)))
    tb_all.write(filename, overwrite=True)