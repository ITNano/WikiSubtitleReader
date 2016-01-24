# -*- coding: utf-8 -*-


from spex_spider import Spex_spider
from raw_to_ass import Raw_to_ass_parser
import os.path #exists
import sys #exit and argv
import codecs #to write utf-8 output
from meta_parser import get_metadata
from preprocess import preprocess_ass




def kupletter_to_ass(username,password,outfilename):
    #urls to fetch kupletter from
    kuplett_URLs=[r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Presentationskuplett_(2016)',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Att_styra_en_stad',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Evig_prakt-final',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Spanar_in_varandra',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Ond_K%C3%A4rlek',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:F%C3%B6rtalfinal',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:F%C3%B6rtalfinal',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:M%C3%A4ssa_A_Cappella',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Tyranni-kuplett',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Förhandlingskuplett_(2016)',r'http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Final-final_(2016)','http://f-spexet.se/f-spexet/wiki/index.php/Hemlig:Förhandlingskuplett_omstart']

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

    #open to write ASS output to
    if not os.path.exists(outfilename):
        outfile = codecs.open(outfilename, 'w','utf-8')

    else:
        print("File '"+outfilename+"' already exists. Delete or rename it and try again.")
        sys.exit(1)
    
    #write preamble to the ASS file
    preamble="[Script Info]\
\nTitle: F-spexet 2016\
\nScriptType: v4.00+\
\nWrapStyle: 1\
\nScaledBorderAndShadow: yes\
\nYCbCr Matrix: None\
\nAegisub Scroll Position: 0\
\nAegisub Active Line: 18\
\nAegisub Video Zoom Percent: 1.000000\
\nLast Style Storage: Default\
\nPlayResX: 0\
\nScroll Position: 78\
\nActive Line: 96\
\nVideo Zoom Percent: 1\
\nCollisions: Normal\
\nPlayResY: 0\n\n"

    styles=r"[V4+ Styles]"\
+"\n"+r"Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding"\
+"\n"+r"Style: ALLA,Arial,32,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: KOMMENTAR,Arial,32,&H00000000,&H00000000,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: GILGASHTAR,Arial,32,&H000000FF,&H000000FF,&H000000FF,&H000000FF,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: GILGASHTAR NERE,Arial,32,&H000000FF,&H000000FF,&H000000FF,&H000000FF,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: ENHEDUANNA,Arial,32,&H00FF3399,&H00FF3399,&H00FF3399,&H00FF3399,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: ENHEDUANNA NERE,Arial,32,&H00FF3399,&H00FF3399,&H00FF3399,&H00FF3399,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: HAMMURABI,Arial,32,&H003399FF,&H003399FF,&H003399FF,&H003399FF,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: HAMMURABI NERE,Arial,32,&H003399FF,&H003399FF,&H003399FF,&H003399FF,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: OKÄND,Arial,32,&H0000FFFF,&H0000FFFF,&H0000FFFF,&H0000FFFF,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: ERESHTI-AYA,Arial,32,&H0033CC33,&H0033CC33,&H0033CC33,&H0033CC33,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: ERESHTI-AYA NERE,Arial,32,&H0033CC33,&H0033CC33,&H0033CC33,&H0033CC33,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: GERTRUDE,Arial,32,&H00FF6600,&H00FF6600,&H00FF6600,&H00FF6600,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: GERTRUDE NERE,Arial,32,&H00FF6600,&H00FF6600,&H00FF6600,&H00FF6600,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: TAPPUTI,Arial,32,&H00FFFF00,&H00FFFF00,&H00FFFF00,&H00FFFF00,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: TAPPUTI NERE,Arial,32,&H00FFFF00,&H00FFFF00,&H00FFFF00,&H00FFFF00,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: NAMMU,Arial,32,&H00335C85,&H00335C85,&H00335C85,&H00335C85,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: NAMMU NERE,Arial,32,&H00335C85,&H00335C85,&H00335C85,&H00335C85,0,0,0,0,100,100,0,0,1,2,2,2,50,50,45,1"\
+"\n"+r"Style: ALLA NERE,Arial,32,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,2,2,2,57,50,45,1"\
+"\n"+r"Style: ALLA MITTEN,Arial,32,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n"+r"Style: ALLA STORT,Arial,32,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,&H00FFFFFF,0,0,0,0,100,100,0,0,1,2,2,5,50,50,45,1"\
+"\n\n"

    event_preamble="[Events]\
\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"

    outfile.write(preamble)
    outfile.write(styles)
    outfile.write(event_preamble)

    #parse read text and write to an ASS file
    ass_parser=Raw_to_ass_parser(30,1) #increment 1 second for each new line. Start at 30 seconds.
    #Various short forms of the different styles defined above. 
    #Note that keys are cast to lowercase, and hence no upper case version is needed
    ass_parser.style_dictionary["kommentar"]="KOMMENTAR"
    ass_parser.style_dictionary["alla"]="ALLA"
    ass_parser.style_dictionary["gilgamesh"]="GILGASHTAR"
    ass_parser.style_dictionary["g"]="GILGASHTAR"
    ass_parser.style_dictionary["gil"]="GILGASHTAR"
    ass_parser.style_dictionary["ishtar"]="GILGASHTAR"
    ass_parser.style_dictionary["i"]="GILGASHTAR"
    ass_parser.style_dictionary["ereshti-aya"]="ERESHTI-AYA"
    ass_parser.style_dictionary["ereshti aya"]="ERESHTI-AYA"
    ass_parser.style_dictionary["ereshtiaya"]="ERESHTI-AYA"
    ass_parser.style_dictionary["aya"]="ERESHTI-AYA"
    ass_parser.style_dictionary["a"]="ERESHTI-AYA"
    ass_parser.style_dictionary["nammu"]="NAMMU"
    ass_parser.style_dictionary["n"]="NAMMU"
    ass_parser.style_dictionary["tapputi"]="TAPPUTI"
    ass_parser.style_dictionary["t"]="TAPPUTI"
    ass_parser.style_dictionary["enheduanna"]="ENHEDUANNA"
    ass_parser.style_dictionary["enheduana"]="ENHEDUANNA"
    ass_parser.style_dictionary["e"]="ENHEDUANNA"
    ass_parser.style_dictionary["hammurabi"]="HAMMURABI"
    ass_parser.style_dictionary["h"]="HAMMURABI"
    ass_parser.style_dictionary["gertrude"]="GERTRUDE"
    ass_parser.style_dictionary["gertrude bell"]="GERTRUDE"
    ass_parser.style_dictionary["gertrudebell"]="GERTRUDE"
    ass_parser.style_dictionary["bell"]="GERTRUDE"
    ass_parser.style_dictionary["b"]="GERTRUDE"

    delimiter=':' #separates singer from lyrics

    for lyric in lyrics:  
        #run through the file one time to parse metadata
        meta=get_metadata(lyric,delimiter)
        padding="kommentar:"
        outfile.write(ass_parser.parse_line_to_ass(padding,delimiter)+"\n");ass_parser.increment_time()

        title_line="kommentar: Titel:"+meta.titel
        mel_line="kommentar: Melodi:"+meta.melodi
        auth_line=u"kommentar: Författare:"+meta.forf
        arr_line="kommentar: Arr:"+meta.arr
        medv_line="kommentar: Medverkande:"+meta.medv
        outfile.write(ass_parser.parse_line_to_ass(title_line,delimiter)+"\n");ass_parser.increment_time()
        outfile.write(ass_parser.parse_line_to_ass(mel_line,delimiter)+"\n");ass_parser.increment_time()
        outfile.write(ass_parser.parse_line_to_ass(auth_line,delimiter)+"\n");ass_parser.increment_time()
        outfile.write(ass_parser.parse_line_to_ass(arr_line,delimiter)+"\n");ass_parser.increment_time()
        outfile.write(ass_parser.parse_line_to_ass(medv_line,delimiter)+"\n");ass_parser.increment_time()

        outfile.write(ass_parser.parse_line_to_ass(padding,delimiter)+"\n");ass_parser.increment_time()
        
        #if the first line does not have a singer
        #we will interpret it and following lines as if everyone is singing
        #NOTE: empty lines are intepreted as belonging to the previous singer
        #but we manually override this behavior for the first line only.
        #NOTE: its likely that the preprocessing will remove these lines anyway
        ass_parser.empty_style="ALLA"

        for line in preprocess_ass(lyric,delimiter):
            ass_line=ass_parser.parse_line_to_ass(line,delimiter)
            ass_parser.increment_time()
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
    kupletter_to_ass(sys.argv[1],sys.argv[2],sys.argv[3])
