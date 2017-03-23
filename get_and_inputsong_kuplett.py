# -*- coding: utf-8 -*-

from raw_to_inputsong import Raw_to_inputsong_parser
import os.path #exists
import sys #exit and argv
import codecs #to write utf-8 output
import kuplett_parser
from meta_parser import get_metadata
from preprocess import preprocess_inputsong



def kupletter_to_inputsong(username,password,outdirname):
    sourcefile = "data_2017.txt"
    lyrics=kuplett_parser.get_all_lyrics(sourcefile, username, password);
    #parse read text and write to an inputsong file
    inputsong_parser=Raw_to_inputsong_parser() 

    #Various short forms of the different styles defined above. 
    #Note that keys are cast to lowercase, and hence no upper case version is needed
    data = kuplett_parser.load_data(sourcefile);
    inputsong_parser.style_dictionary = data.get("dictionary")
    inputsong_parser.short_style_dictionary = data.get("shortdictionary");
    print(inputsong_parser.short_style_dictionary);

    delimiter=':' #separates singer from lyrics

    outfilenames = []
    akt = 1
    for page in kuplett_parser.load_data(sourcefile).get("urls"):
        name = kuplett_parser.get_generic_name(page);
        outfilenames.append("Akt"+str(akt)+"/"+name+".txt")
        if "final" in name.lower():
            # This is kind of dangerous. Assumes that all songs with 'final'
            # in the same is the last song of each akt (part) of the spex.
            akt += 1
    
    i=0
    for lyric in lyrics:
        #open relevant file
        outfilename=outdirname+"/"+outfilenames[i]
        folder = outfilename;
        if folder.find("/") >= 0:
            folder = folder[:folder.rfind("/")]
        if not os.path.exists(folder):
            try:
                os.makedirs(folder);
            except OSError:
                print("Skipping creation of %s because it exists already.", folder)
        outfile = codecs.open(outfilename, 'w','utf-8')
    
        #First we go through the lyric to get metadata that's
        #potentially been sprinkled throughout the text (bad spexare!)
        meta=get_metadata(lyric,delimiter)

        title_line=meta.titel
        mel_line=meta.melodi
        auth_line=meta.forf
        arr_line=meta.arr
        medv_line=meta.medv
        outfile.write(title_line+"\n")
        outfile.write(mel_line+"\n")
        outfile.write(auth_line+"\n")
        outfile.write(medv_line+"\n")
        outfile.write(arr_line+"\n")
        outfile.write("\n")
    
        #if the first line does not have a singer
        #we will interpret it and following lines as if everyone is singing
        #NOTE: empty lines are intepreted as belonging to the previous singer
        #but we manually override this behavior for the first line only.
        inputsong_parser.empty_style="Alla"

        for line in preprocess_inputsong(lyric,delimiter):
            inputsong_line=inputsong_parser.parse_line_to_inputsong(line,delimiter)
            outfile.write(inputsong_line+"\n")

        i=i+1
        outfile.close()

if __name__ == "__main__":
    if len(sys.argv)<4:
        print("Need 3 arguments.")
        print("Usage:")
        print("get_and_parse_kuplett.py USERNAME PASSWORD OUTDIR_NAME")
        sys.exit(3)
    kupletter_to_inputsong(sys.argv[1],sys.argv[2],sys.argv[3])
