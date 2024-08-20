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
import sqlite3
import shutil
import argparse
from pathlib import Path
from acronym_gui import read_acronyms
# ===============================================================
# Functions
# ===============================================================
# Function to add a new acronym
def add_acronym(acronym, translation, description=None):
    # Connect to the SQLite database
    conn = sqlite3.connect('database/acronyms.db')
    cursor = conn.cursor()

    # Check if the acronym already exists
    cursor.execute("SELECT COUNT(*) FROM Acronyms WHERE acronym = ?", (acronym,))
    acronym_exists = cursor.fetchone()[0]

    if acronym_exists:
        # Acronym exists, now check if the translation exists
        cursor.execute("""
            SELECT COUNT(*) FROM Acronyms WHERE acronym = ? AND translation = ?
        """, (acronym, translation))
        translation_exists = cursor.fetchone()[0]

        if translation_exists:
            print(f"The acronym '{acronym}' with the translation '{translation}' already exists.")
        else:
            # Insert the new translation for the existing acronym
            cursor.execute("""
                INSERT INTO Acronyms (acronym, translation, description) VALUES (?, ?, ?)
            """, (acronym, translation, description))
            print(f"Added new translation for '{acronym}': '{translation}'")
    else:
        # Acronym does not exist, insert both acronym and translation
        cursor.execute("""
            INSERT INTO Acronyms (acronym, translation, description) VALUES (?, ?, ?)
        """, (acronym, translation, description))
        print(f"Added new acronym '{acronym}' with translation '{translation}'")

    # Commit changes and close the connection
    conn.commit()
    conn.close()


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
tb_add = read_acronyms(table_filename)
if tb_add.colnames[0]=='\ufeffAcronym':
    tb_add.rename_column('\ufeffAcronym', 'Acronym')


shutil.copy('database/acronyms.db', 'database/acronyms_backup.db')
# Connect to your SQLite database
conn = sqlite3.connect('database/acronyms.db')
cursor = conn.cursor()

# Example Usage
for tb in tb_add:
    add_acronym(tb['Acronym'], tb['Translation'], tb['Description'])


# Close the connection when done
conn.close()