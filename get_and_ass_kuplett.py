# -*- coding: utf-8 -*-

from wiki_to_text import wiki_to_text
from texts_to_ass import texts_to_ass
import sys

def kupletter_to_ass(username,password,outfilename,sourcefile = "data_2019.txt"):
    textdirname="texts"
    wiki_to_text(username,password,textdirname,sourcefile)
    texts_to_ass(textdirname,outfilename,sourcefile)

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("Need 3 arguments.")
        print("Usage:")
        print("get_and_parse_kuplett.py USERNAME PASSWORD OUTFILE_NAME")
        sys.exit(3)
    #if os.path.exists(sys.argv[3]):
     #   print("File '"+sys.argv[3]+"' already exists. Delete or rename it and try again.")
      #  sys.exit(1)
    kupletter_to_ass(sys.argv[1], sys.argv[2], sys.argv[3])
