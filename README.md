# WikiSubtitleReader
Parses subtitles for F-spexet from their wiki page into different formats, such as an .ass file etc.
Note: Authentication to the private material is required for this to be run.


## Running the script(s)
To generate an ass file, call:

*python3 get_and_ass_kuplett.py <USERNAME> <PASSWORD> <OUTPUT ASS FILE>*

To generate a folder structure, call:

*python3 get_and_inputsong_kuplett.py <USERNAME> <PASSWORD> <OUTPUT DIR>*

This will populate subdirs

Akt1

Akt2

Akt3

with one file for each song.

Note that Python 3.x is used. Python 2.x will have syntax errors.

## Diff functionality
For each time the scripts syncs data, a raw file is stored to be able to calculate
a diff. If you wish to resync without diff data, please remove the folder "diff"
before running the script. To resync a particular song without diff data, please
remove only that particualar file from the diff folder.

Note that any changes in the .ass file will remain there unless the corresponding
line is changed on the wiki. This means that custom styling can be made to lines
(and remain) unless the concrete content is changed on the wiki.

## Requirements
Requires Python3 and selenium 3.3 (http://www.seleniumhq.org/):

         (sudo) pip(3) install selenium

Geckodriver for newer versions of firefox

          https://github.com/mozilla/geckodriver/releases
          extract the appropriate binary and put it in your PATH
