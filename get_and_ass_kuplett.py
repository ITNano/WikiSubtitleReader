# -*- coding: utf-8 -*-

from raw_to_ass import Raw_to_ass_parser
import os.path #exists
import sys #exit and argv
import codecs #to write utf-8 output
import kuplett_parser
from meta_parser import get_metadata
from preprocess import preprocess_ass


def kupletter_to_ass(username,password,outfilename):
    sourcefile = "data_2016.txt"

    lyrics=kuplett_parser.get_all_lyrics(sourcefile, username, password);

    #open to write ASS output to
    if not os.path.exists(outfilename):
        outfile = codecs.open(outfilename, 'w','utf-8')
    else:
        print("File '"+outfilename+"' already exists. Delete or rename it and try again.")
        sys.exit(1)
    
    #write preamble to the ASS file
    outfile.write(kuplett_parser.get_ass_header(sourcefile))

    #parse read text and write to an ASS file
    ass_parser=Raw_to_ass_parser(30,1) #increment 1 second for each new line. Start at 30 seconds.
    
    # Load dictionary for mapping singers
    data = kuplett_parser.load_data(sourcefile);
    ass_parser.style_dictionary=data.get("dictionary")
    if "multilinesplitter" in data.get("meta").keys():
        ass_parser.multi_line_keyword = data.get("meta").get("multilinesplitter")

    delimiter=':' #separates singer from lyrics

    for lyric in lyrics:  
        #run through the file one time to parse metadata
        meta=get_metadata(lyric,delimiter)
        padding="kommentar:"
        outfile.write(ass_parser.parse_line_to_ass(padding,delimiter)+"\n");

        title_line="kommentar: Titel:"+meta.titel
        mel_line="kommentar: Melodi:"+meta.melodi
        auth_line=u"kommentar: Författare:"+meta.forf
        arr_line="kommentar: Arr:"+meta.arr
        medv_line="kommentar: Medverkande:"+meta.medv
        outfile.write(ass_parser.parse_line_to_ass(title_line,delimiter)+"\n");
        outfile.write(ass_parser.parse_line_to_ass(mel_line,delimiter)+"\n");
        outfile.write(ass_parser.parse_line_to_ass(auth_line,delimiter)+"\n");
        outfile.write(ass_parser.parse_line_to_ass(arr_line,delimiter)+"\n");
        outfile.write(ass_parser.parse_line_to_ass(medv_line,delimiter)+"\n");

        outfile.write(ass_parser.parse_line_to_ass(padding,delimiter)+"\n");
        
        #if the first line does not have a singer
        #we will interpret it and following lines as if everyone is singing
        #NOTE: empty lines are intepreted as belonging to the previous singer
        #but we manually override this behavior for the first line only.
        #NOTE: its likely that the preprocessing will remove these lines anyway
        ass_parser.empty_style="ALLA"

        for line in preprocess_ass(lyric,delimiter):
            ass_line=ass_parser.parse_line_to_ass(line,delimiter)
            if len(ass_line) > 0:
                outfile.write(ass_line+"\n")

    outfile.close()

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("Need 3 arguments.")
        print("Usage:")
        print("get_and_parse_kuplett.py USERNAME PASSWORD OUTFILE_NAME")
        sys.exit(3)
    if os.path.exists(sys.argv[3]):
        print("File '"+sys.argv[3]+"' already exists. Delete or rename it and try again.")
        sys.exit(1)
    kupletter_to_ass(sys.argv[1], sys.argv[2], sys.argv[3])
