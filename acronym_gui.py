#!/usr/bin/env python
"""GUI for a LISA Acronym Dicitonary"""
#########################################################################
# IDENT			acronym_gui.py
# LANGUAGE		Python
# AUTHOR		N. Luetzgendorf
# PURPOSE       This is a gui to search for LISA acronyms
#				It uses Tkinter and a csv file with the acronyms
#				to search and provide a translation to acronyms related
#				to LISA (Laser Interferometer Space Antenna).
#
#
# usage: acronym_gui.py [-h]
#
#
# optional arguments:
#   -h, --help            show this help message and exit
#
# VERSION
# 1.0.0 08.09.2021 NL Creation
# 1.0.1 08.09.2021 NL Update
#   1) Added a line break for very long acronyms
#   2) Adding a message about how many acronyms we have
#      (maybe I want to write this in the GUI directly)
#########################################################################
# ===============================================================
# Imports
# ===============================================================
from tkinter import *
from astropy.io import ascii
import numpy as np
from pathlib import Path
# ===============================================================
# Module-wide variables
# ===============================================================
_name = "acronym_gui.py"
_codename = _name.split('.py')[0]
_version = "1.0.1"
__all__ = ['read_acronyms', 'find_word', 'dict']
ASSETS_PATH = Path(__file__).resolve().parent / "assets"
MAXL = 30

# ===============================================================
# Functions
# ===============================================================
def read_acronyms(filename):
    """ Function to read the acronym table

    The csv file needs to have three columns with the
    titles: 'Acronym', 'Translation', 'Description'

    Parameters
    ----------
    filename : str
        Path and filename of csv file.

    Returns
    -------
    tb_all : astropy.table
        Table of the acronyms.

    """
    tb_all = ascii.read(filename, format='csv', encoding='utf-8')
    return tb_all


def find_word(tb_all, word):
    """ Function to find an acronym in the table

    Parameters
    ----------
    tb_all : astropy.table
        Table with all the acronyms as described in read_acronyms.
    word : str
        Acronym (can be lower or upper case) that is being searched.

    Returns
    -------
    trans, descr : str
        Translation and Description of the acronym.
        If not found, those strings are empty.

    """
    # First find the acronym in the table, ignore case
    # (accronyms in the table are all upper case)
    find = tb_all['Acronym'] == word.upper()
    # If it was found, extract Translation and Description
    if np.sum(find) > 0:
        trans = tb_all['Translation'][find].data
        descr = tb_all['Description'][find].data
        # If ther is no description, return and empty string
        descr[descr.mask] = ''
        return trans, descr
    # If it was not found return the empty strings.
    else:
        print('Did not find {:s}'.format(word))
        return ['Did not find {:s}'.format(word)], ['']


def dict():
    """ Function to populate the GUI fields with the right outcome

    Returns
    -------

    """
    # Clearing all fields:
    # Delete the description text if there is any
    descripton.delete("1.0", "end")
    descripton2.delete("1.0", "end")
    descr_title.config(text='')
    descr_title2.config(text='')
    meaning.config(text='')
    meaning2.config(text='')
    # Search the table for the acronym
    trans, descr = find_word(tb_all, word.get())
    # Write description title and content in the text box
    # The first one:
    if descr[0] == '':
        # Remove the title if we don't have any description
        descr_title.config(text='')
    else:
        descr_title.config(text='Description')
        descripton.insert(END, descr[0])

    if len(trans[0])>MAXL:
        # Probably the weirdest way of a line break ever, but it works
        find = [s==' ' for s in trans[0]]
        indices = np.arange(len(trans[0]))[find]
        ibreak = indices[max(np.where(indices < MAXL)[0])]
        meaning.config(text='{} \n {}'.format(trans[0][:ibreak], trans[0][ibreak:]))
    else:
        meaning.config(text=trans[0])

    # See if there is a second one:
    if len(trans) > 1:
        # The first one:
        if descr[1] == '':
            # Remove the title if we don't have any description
            descr_title2.config(text='')
        else:
            descr_title2.config(text='Description')
            descripton2.insert(END, descr[1])

        if len(trans[1])>MAXL:
            # Probably the weirdest way of a line break ever, but it works
            find = [s==' ' for s in trans[1]]
            indices = np.arange(len(trans[1]))[find]
            ibreak = indices[max(np.where(indices < MAXL)[0])]
            meaning2.config(text='{} \n {}'.format(trans[1][:ibreak], trans[1][ibreak:]))
        else:
            meaning2.config(text=trans[1])

        root.geometry("500x700")
        search_button.place(x=160, y=620, width=180, height=56)
    else:
        root.geometry("500x500")
        search_button.place(x=160, y=420, width=180, height=56)


# ===============================================================
# ===========================  MAIN  ============================
# ===============================================================
if __name__ == '__main__':
    # Read the table of acronyms
    filename = Path(__file__).resolve().parent / 'tables/LISA_acronyms.csv'
    tb_all = read_acronyms(filename)

    print('Welcome! We currently have {:d} acronyms on file!'.format(len(tb_all)))

    # Initialize Tkinter
    root = Tk()

    # Set geometry and attributes of main window
    root.geometry("500x500")
    root.configure(bg="white")
    root.title("LISA Acronym Dictionary")

    # Create a white canvas
    canvas = Canvas(root, bg="white", height=750, width=500, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)

    # Set the title image
    title_image = PhotoImage(file=ASSETS_PATH / "title_image.png")
    title = canvas.create_image(250, 80, image=title_image)

    # Set the entry text box to write the acronyms in
    text_box_bg = PhotoImage(file=ASSETS_PATH / "TextBox_Bg.png")
    token_entry_img = canvas.create_image(250, 187.5, image=text_box_bg)
    canvas.create_text(90.0, 170.0, text="Acronym", fill="#515486",
                       font=("Arial-BoldMT", int(13.0)), anchor="w")
    # Here we enter the word
    word = Entry(bd=0, bg="#F6F7F9", highlightthickness=0)
    word.place(x=90, y=180, width=321.0, height=35)
    word.focus()
    # We also bind the enter key to the entry so that we can search with hitting ENTER/RETURN
    word.bind('<Return>', (lambda event: dict()))

    # Creating Frame 1 - for the first spelled out acronym
    frame1 = Frame(root, bg='White')
    meaning = Label(frame1, text="", font=("Helvetica 25 bold"), fg="#26DE7B", bg='white')
    meaning.pack()
    frame1.place(x=250, y=260, anchor='center')

    # Creating Frame 2 - for the first description of the acronym
    frame2 = Frame(root, bg='White')
    descr_title = Label(frame2, text="", font=("Helvetica 10 bold"), bg='White', fg='dark grey')
    descr_title.pack(side=TOP)
    descripton = Text(frame2, height=5, width=49, font=("Helvetica 12"),
                      wrap='word', bg='White', fg='#4D4D4D', borderwidth=0, highlightthickness=0)
    descripton.pack()
    frame2.place(x=50, y=300, width=400, height=200)

    # Creating Frame 3 - for the second spelled out acronym
    frame3 = Frame(root, bg='White')
    meaning2 = Label(frame3, text="", font=("Helvetica 25 bold"), fg="#26DE7B", bg='white')
    meaning2.pack()
    frame3.place(x=250, y=500, anchor='center')

    # Creating Frame 4 - for the second description of the acronym
    frame4 = Frame(root, bg='White')
    descr_title2 = Label(frame4, text="", font=("Helvetica 10 bold"), bg='White', fg='dark grey')
    descr_title2.pack(side=TOP)
    descripton2 = Text(frame4, height=5, width=49, font=("Helvetica 12"),
                      wrap='word', bg='White', fg='#4D4D4D', borderwidth=0, highlightthickness=0)
    descripton2.pack()
    frame4.place(x=50, y=540, width=400, height=200)

    # Add the search button
    search_button_img = PhotoImage(file=ASSETS_PATH / "search_button_green.png")
    search_button = Button(
        image=search_button_img, borderwidth=0, highlightthickness=0,
        command=dict, relief="flat")
    search_button.place(x=160, y=420, width=180, height=56)

    # Execute Tkinter
    root.mainloop()
