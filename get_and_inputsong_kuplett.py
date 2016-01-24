# -*- coding: utf-8 -*-


from spex_spider import Spex_spider
from raw_to_inputsong import Raw_to_inputsong_parser
import os.path #exists
import sys #exit and argv
import codecs #to write utf-8 output
from meta_parser import get_metadata
from preprocess import preprocess_inputsong



def kupletter_to_inputsong(username,password,outdirname):
    #urls to fetch kupletter from
    kuplett_URLs=[r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Presentationskuplett_(2016)',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Att_styra_en_stad',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Evig_prakt-final',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Spanar_in_varandra',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Ond_K%C3%A4rlek',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:M%C3%A4ssa_A_Cappella',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:F%C3%B6rtalfinal',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Tyranni-kuplett',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Förhandlingskuplett_(2016)',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Final-final_(2016)','http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Förhandlingskuplett_omstart']

    outfilenames=[r'Akt1/presentationskuplett.txt',r'Akt1/attStyraEnStad.txt',r'Akt1/evigPraktFinal.txt',r'Akt2/spanarInVarandra.txt',r'Akt2/ondKarlek.txt',r'Akt2/massaACappella.txt',r'Akt2/fortalfinal.txt',r'Akt3/tyranniKuplett.txt',r'Akt3/forhandlingskuplett.txt',r'Akt3/finalFinal.txt',r'Omstarter/forhandlingOmstart.txt']

    #login to f-spexet/wiki NOTE: this depends on implementation details of
    #the mediawiki, but it works as of 2015-11-03
    #NOTE: Firefox is the only supported driver so far. Trivial to add other browsers supported by Selenium, though.
    spider=Spex_spider(username,password,"Firefox") 

    lyrics=[] #will become the list of list of lines of kupletter
    #to skip first and last lines of the text body
    #This might be useful, since those should/could contain metadata.
    exclude_first=0;
    exclude_last=0;

    for url in kuplett_URLs:
        #get body text in one big string suitable for human reading.
        text=spider.get_text_body(url)
        #Break the text into a list of strings, one for each line.
        textlist=text.splitlines()
        first=0+exclude_first
        last=len(textlist)-exclude_last
        kuplett_text=textlist[first:last]
        lyrics.append(kuplett_text)


    
    #parse read text and write to an inputsong file
    inputsong_parser=Raw_to_inputsong_parser() 

    #Various short forms of the different styles defined above. 
    #Note that keys are cast to lowercase, and hence no upper case version is needed
    inputsong_parser.style_dictionary["alla"]="Alla"
    inputsong_parser.style_dictionary["gilgamesh"]="Gilgamesh"
    inputsong_parser.style_dictionary["g"]="Gilgamesh"
    inputsong_parser.style_dictionary["gil"]="Gilgamesh"
    inputsong_parser.style_dictionary["ishtar"]="Ishtar"
    inputsong_parser.style_dictionary["i"]="Ishtar"
    inputsong_parser.style_dictionary["ereshti-aya"]="Ereshti-Aya"
    inputsong_parser.style_dictionary["ereshti aya"]="Ereshti-Aya"
    inputsong_parser.style_dictionary["ereshtiaya"]="Ereshti-Aya"
    inputsong_parser.style_dictionary["aya"]="Ereshti-Aya"
    inputsong_parser.style_dictionary["a"]="Ereshti-Aya"
    inputsong_parser.style_dictionary["nammu"]="Nammu"
    inputsong_parser.style_dictionary["n"]="Nammu"
    inputsong_parser.style_dictionary["tapputi"]="Tapputi"
    inputsong_parser.style_dictionary["t"]="Tapputi"
    inputsong_parser.style_dictionary["enheduanna"]="Enheduana"
    inputsong_parser.style_dictionary["enheduana"]="Enheduana"
    inputsong_parser.style_dictionary["e"]="Enheduana"
    inputsong_parser.style_dictionary["hammurabi"]="Hammurabi"
    inputsong_parser.style_dictionary["h"]="Hammurabi"
    inputsong_parser.style_dictionary["gertrude"]="Gertrude"
    inputsong_parser.style_dictionary["gertrude bell"]="Gertrude"
    inputsong_parser.style_dictionary["gertrudebell"]="Gertrude"
    inputsong_parser.style_dictionary["bell"]="Gertrude"
    inputsong_parser.style_dictionary["b"]="Gertrude"

    delimiter=':' #separates singer from lyrics

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
