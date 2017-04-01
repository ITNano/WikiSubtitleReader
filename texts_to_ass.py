# -*- coding: utf-8 -*-

from read_texts import read_texts
from raw_to_ass import Raw_to_ass_parser
import os.path #exists
import sys #exit and argv
import codecs #to write utf-8 output
import kuplett_parser
import diff_tool
from meta_parser import get_metadata
from preprocess import preprocess_ass


def texts_to_ass(textdirname,outfilename,sourcefile):
    allowEmptyLines = True
    lyrics = read_texts(textdirname)
    #parse read text and write to an ASS file
    ass_parser=Raw_to_ass_parser(30,1) #increment 1 second for each new line. Start at 30 seconds.
    
    # Load dictionary for mapping singers
    data = kuplett_parser.load_data(sourcefile);
    ass_parser.style_dictionary=data.get("dictionary")
    if "multilinesplitter" in data.get("meta").keys():
        ass_parser.multi_line_keyword = data.get("meta").get("multilinesplitter")

    delimiter=':' #separates singer from lyrics

    counter = 0
    fileContent = "";
    currentOldContentOffset = 0
    for lyric in lyrics:
        #run through the file one time to parse metadata
        meta=get_metadata(lyric,delimiter)
        padding="kommentar:"
        fileContent += ass_parser.parse_line_to_ass(padding,delimiter,allowEmptyLines)+"\n"

        title_line="kommentar: Titel:"+meta.titel
        mel_line="kommentar: Melodi:"+meta.melodi
        auth_line=u"kommentar: Författare:"+meta.forf
        arr_line="kommentar: Arr:"+meta.arr
        medv_line="kommentar: Medverkande:"+meta.medv
        fileContent += ass_parser.parse_line_to_ass(title_line,delimiter,allowEmptyLines)+"\n"
        fileContent += ass_parser.parse_line_to_ass(mel_line,delimiter,allowEmptyLines)+"\n"
        fileContent += ass_parser.parse_line_to_ass(auth_line,delimiter,allowEmptyLines)+"\n"
        fileContent += ass_parser.parse_line_to_ass(arr_line,delimiter,allowEmptyLines)+"\n"
        fileContent += ass_parser.parse_line_to_ass(medv_line,delimiter,allowEmptyLines)+"\n"

        fileContent += ass_parser.parse_line_to_ass(padding,delimiter,allowEmptyLines)+"\n"
        
        #if the first line does not have a singer
        #we will interpret it and following lines as if everyone is singing
        #NOTE: empty lines are intepreted as belonging to the previous singer
        #but we manually override this behavior for the first line only.
        #NOTE: its likely that the preprocessing will remove these lines anyway
        ass_parser.empty_style="ALLA"
        newContent = preprocess_ass(lyric,delimiter)
        for line in newContent:
            ass_line=ass_parser.parse_line_to_ass(line,delimiter,allowEmptyLines)
            if len(ass_line) > 0:
                fileContent += ass_line+"\n"

        # # Read data from old file (if such exists)
        # useOldFile, oldContent, oldContentOffset = getOldData(filename, outfilename, currentOldContentOffset)
        # currentOldContentOffset = oldContentOffset
        # # Find diff in files
        # diff = diff_tool.find_unchanged_lines(filename, lyric, allowEmptyLines)
        # # Fetch the new data
        # newContent = preprocess_ass(lyric,delimiter)
        # # Process each diff.
        # for d in diff:
        #     if d.isNewLine or not useOldFile:
        #         ass_line=ass_parser.parse_line_to_ass(newContent[d.line],delimiter,allowEmptyLines)
        #         if len(ass_line) > 0:
        #             fileContent += ass_line+"\n"
        #     else:
        #         if d.line+oldContentOffset >= len(oldContent):
        #             print("Dammit, now we are outside the valid intervals. Did anyone change the header size? (title etc.) See getOldData() for fix.")
        #         fileContent += oldContent[d.line+oldContentOffset]
    
    #open to write ASS output to
    if len(os.path.dirname(outfilename).strip()) > 0 and not os.path.exists(os.path.dirname(outfilename)):
        os.makedirs(os.path.dirname(outfilename))
    outfile = codecs.open(outfilename, 'w','utf-8')
    
    #write preamble to the ASS file
    outfile.write(kuplett_parser.get_ass_header(sourcefile))
    #write content
    outfile.write(fileContent)
    outfile.close()
    
def getOldData(sourcefile, outfile, prevOffset):
    if diff_tool.has_diff(sourcefile):
        if not os.path.exists(outfile):
            print("Found diff file but not previous version of the .ass file. Please remove diff file.")
            sys.exit(1)
        else:
            oldFile = codecs.open(outfile, 'r', 'utf-8')
            oldContent = oldFile.readlines()
            oldContentOffset = prevOffset
            for line in oldContent[prevOffset:]:
                if not "KOMMENTAR,,0,0,0,,Titel:" in line.strip():
                    oldContentOffset += 1
                else:
                    break
            return (True, oldContent, oldContentOffset+6)               # TODO get a better way to determine header size
    else:
        if not os.path.exists(outfile):
            return (False, None, None)
        else:
            oldFile = codecs.open(outfile, 'r', 'utf-8')
            oldContent = oldFile.readlines()
            oldContentOffset = prevOffset
            for line in oldContent[prevOffset:]:
                if not "KOMMENTAR,,0,0,0,,Titel:" in line.strip():
                    oldContentOffset += 1
                else:
                    break
            return (False, None, oldContentOffset+6)               # TODO get a better way to determine header size

if __name__ == "__main__":
    if len(sys.argv)<3:
        print("Need 2 arguments.")
        print("Usage:")
        print("texts_to_ass.py TEXT_DIRNAME OUTFILE_NAME")
        sys.exit(3)
    texts_to_ass(sys.argv[1], sys.argv[2],"data_2017.txt")
