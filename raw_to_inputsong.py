# -*- coding: utf-8 -*-
#Python class to parse lyrics on the form
#Singer 1: I am so happy, hear me sing
#And write it to a .txt file parseable by 'inputsongpackage.sty'
#The string before the separator ':' is used to format the text by mapping it to
#a predefined format, the remainder is the actual text to sing.

import re #regular expressions


class Raw_to_inputsong_parser():


    def parse_line_to_inputsong(self,line,delimiter):
        #Note that keys are all cast to lowercase.
        split_line=line.split(delimiter,1)
        #generally, we do not want to write out the singer on every line
        #only when the singer changes, or if the last was empty
        if len(line) == 0:
            return ""
        if len(split_line)==1:
            #if no singer is specified
            #we will assume that it's the last one
            #and not write out a singer
            if split_line[0].strip()=='':
                #it might also be a completely empty line,
                #after which any singer will be printed
                self.last_singer=''
                return '' #preserve empty lines
            return split_line[0].strip()
        if split_line[0]==self.last_singer:
            #if the singer is explicitly specified and the last one
            return split_line[1].strip()

        #here we actually have to explicitly specify the singer
        #lines with multiple singers can be split at "," or "+" at the moment.
        #lines with more than max_singers will be printed as "Alla"
        #lines with more than 1 and less than max_singers will use the sanctioned short forms of the names
        max_singers=2
        if ("," or "+") in split_line[0]:
            result = ""
            singers=re.split('[,+]',split_line[0])
            #print(singers)
            if len(singers)>max_singers:
                result += self.style_dictionary.get("alla", r"OKÄND")+',' #trailing , stripped later
            else:
                for singer in singers:
                    result += self.short_style_dictionary[self.style_dictionary.get(singer.lower().strip(), r"OKÄND")]+","
            return result[:-1]+":"+split_line[1].strip()
        else:
            #single singer. Do not print out comment lines
            if self.style_dictionary.get(split_line[0].lower(), r"OKÄND")=="KOMMENTAR":
                return ""
            else:
                return self.short_style_dictionary[self.style_dictionary.get(split_line[0].lower(), r"OKÄND")]+":"+split_line[1].strip()

    def __init__(self):
        self.style_dictionary={}
        self.empty_style=""
        self.last_singer=""



