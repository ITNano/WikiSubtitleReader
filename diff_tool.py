# Contains diff functionality

import re
import codecs
import kuplett_parser
import os.path
import preprocess

class DiffData():
    def __init__(self, line, isNewLine):
        self.line = line
        self.isNewLine = isNewLine

def find_unchanged_lines(sourcename, content, allowEmptyLines):
    content = preprocess.preprocess_general(content, ':')

    result = []
    filename = get_diff_filename(sourcename)
    if os.path.exists(filename):
        file = codecs.open(filename, 'r', 'utf-8')
        counterContent = 0
        counterPrev = 0
        prevLines = file.readlines()
        for line in content:
            if allowEmptyLines or len(line) > 0:
                foundMatch = False
                line = line.strip()
                for index in range(counterPrev, len(prevLines)):
                    if line == prevLines[index].strip():
                        result.append(DiffData(index, False))
                        counterPrev = index+1
                        foundMatch = True
                        break
                
                if not foundMatch:
                    result.append(DiffData(counterContent, True))
                
            counterContent += 1
            
    else:
        counter = 0
        for line in content:
            if allowEmptyLines or len(line.strip()) > 0:
                result.append(DiffData(counter, True))
            counter += 1
                
    # Save data to next time
    if len(os.path.dirname(filename).strip()) > 0 and not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
       
    outfile = codecs.open(filename, 'w', 'utf-8')
    for line in content:
        outfile.write(line+"\n")
    
    return result
    
def has_diff(sourcefile):
    return os.path.exists(get_diff_filename(sourcefile))
    
def get_diff_filename(sourcefile):
    return "diff/"+kuplett_parser.get_generic_name(sourcefile)