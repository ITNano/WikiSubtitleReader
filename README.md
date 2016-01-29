# WikiSubtitleReader
Parses subtitles for F-spexet from their wiki page into different formats, such as an .ass file etc.
Note: Authentication to the private material is required for this to be run.


## Running the script(s)
To generate an ass file, call:

*python get_and_ass_kuplett.py <USERNAME> <PASSWORD> <OUTPUT ASS FILE>*

To generate a folder structure, call:

*python get_and_inputsong_kuplett.py <USERNAME> <PASSWORD> <OUTPUT DIR>*

This will populate subdirs

Akt1

Akt2

Akt3

with one file for each song.

## Requirements
Requires selenium for python (http://www.seleniumhq.org/):

(sudo) pip install selenium
