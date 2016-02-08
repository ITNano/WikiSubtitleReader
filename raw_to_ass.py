# -*- coding: utf-8 -*-
#Python class to parse lyrics on the form
#Singer 1: I am so happy, hear me sing
#And write it to an .ass file. (Advanced SubStation Alpha subtitle file)
#The string before the separator ':' is used to format the text by mapping it to
#a predefined format, the remainder is the actual text to sing.
import math

def time_to_seconds(time):
    hmmss_list=time.split(':')
    seconds=3600*float(hmmss_list[0])+60*float(hmmss_list[1])+float(hmmss_list[2])
    return seconds

def seconds_to_time(seconds):
    #Seconds are given with two decimal points. 1 digit for hours.
    #Minutes and hours are integers.
    hours=math.floor(seconds/3600)
    seconds=seconds-3600*hours
    minutes=math.floor(seconds/60)
    seconds=seconds-60*minutes    
    seconds=float("{0:05.2f}".format(seconds))
    if seconds==60:
        seconds=0;
        minutes=minutes+1;
        if minutes==60:
            minutes=0
            hours=hours+1
    #Pads minutes with a leading zero, formats seconds to xx.xx
    hmmss_string="{0:01.0f}".format(hours)+':'+"{0:02.0f}".format(minutes)+':'+"{0:05.2f}".format(seconds)
    return hmmss_string

class Raw_to_ass_parser():


    def parse_line_to_ass(self,line,delimiter):
        #example output:
        #Dialogue: 0,0:00:26.00,0:00:27.00,CHARACTER,,0,0,0,,I am singing!
        #Styledict maps a short form to a style used in the ASS file. Example:
        #Styledict["a"]="ANNA"
        #Note that keys are all cast to lowercase.
        if len(line) == 0:
            line = "kommentar:"                 # keep empty lines but do not show
            
        split_line=line.split(delimiter,1)
        # Handle lines without explicitly written singer
        if len(split_line)==1:
            split_line=[self.empty_style,split_line[0]]
        
        # Handle multi/none singer(s)
        default_singer = r"OKÄND"
        if "," in split_line[0]:
            default_singer = r"ALLA"
        
        # Handle people singing at the same time
        extra_stylepart = ""
        if self.multi_line:
            extra_stylepart = " NERE"
        if split_line[1].strip().endswith(self.multi_line_keyword):
            split_line[1] = split_line[1].strip()[:-len(self.multi_line_keyword)]
            self.multi_line = True;
        else:
            self.multi_line = False;
        
        # Construct the actual data.
        outline='Dialogue: 0,'+self.time_start+','+self.time_end+','
        outline=outline+self.style_dictionary.get(split_line[0].lower(), default_singer)+extra_stylepart+',,0,0,0,,'+split_line[1].strip()
        
        # Prepare for next line
        self.empty_style=split_line[0]
        if len(outline) > 0 and not self.multi_line:
            self.increment_time()
            
        return outline


    def increment_time(self):
        float_start=time_to_seconds(self.time_start)
        float_end=time_to_seconds(self.time_end)
        self.time_start=seconds_to_time(float_start+self.time_step)
        self.time_end=seconds_to_time(float_end+self.time_step)

    def __init__(self,start_time,increment_time):
        self.time_step=float(increment_time)
        self.time_start=seconds_to_time(start_time)
        self.time_end=seconds_to_time(time_to_seconds(self.time_start)+self.time_step)
        self.style_dictionary={}
        self.empty_style=""
        self.multi_line = False;
        self.multi_line_keyword = "[samtidigt]"



