# LISA Acronym Dictionary

Welcome to the LISA Acronym Dictionary. I created this out of frustration about the many acronyms used in this project. The screenshot below shows how the GUI looks like on a MacOSX, I don't know how it looks on a different OS, but happy for feedback. 

![Screenshof of the GUI](./screenshots/gui1.png?raw=true "Optional Title")

To run the GUI you simply clone this repository and run the `acronym_gui.py` either outside or inside of Python. You should be able to type your acronym in the input field and hit enter (or use the search button). If you want to add more acronyms to the list edit the [LISA_acronyms.csv](LISA_acronyms.csv) file (I recommend in Excel), if possible also adding a short description.

If you have another long table of acronyms and you want to merge it with the existing list (recommended method), you can use `merge_tables.py [TABLENAME]` using a csv table with the fields Acronym, Translation, Description (on MacOS the table needs to be saved as a normal csv and not UTF-8, make sure there are no weird charactes in there).