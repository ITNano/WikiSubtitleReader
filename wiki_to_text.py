# -*- coding: utf-8 -*-

from raw_to_ass import Raw_to_ass_parser
import os.path #exists
import sys #exit and argv
import codecs #to write utf-8 output
import kuplett_parser
import diff_tool
from meta_parser import get_metadata
from preprocess import preprocess_ass

def wiki_to_text(username,password,outputdir,sourcefile):
    lyrics=kuplett_parser.get_all_lyrics(sourcefile, username, password);
    data = kuplett_parser.load_data(sourcefile)

    counter = 0
    for lyric in lyrics:
        filename = outputdir + "/" + kuplett_parser.get_generic_name(data.get("urls")[counter])
        counter += 1
    
        if len(os.path.dirname(filename).strip()) > 0 and not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        outfile = codecs.open(filename, 'w', 'utf-8')
        for line in lyric:
            outfile.write(line+"\n")
    return lyrics
        
if __name__ == "__main__":
    if len(sys.argv)<4:
        print("Need 3 arguments.")
        print("Usage:")
        print("get_and_parse_kuplett.py USERNAME PASSWORD OUTFILE_NAME")
        sys.exit(3)
    #if os.path.exists(sys.argv[3]):
     #   print("File '"+sys.argv[3]+"' already exists. Delete or rename it and try again.")
      #  sys.exit(1)
    wiki_to_text(sys.argv[1], sys.argv[2], sys.argv[3],sourcefile="data_2017.txt")
