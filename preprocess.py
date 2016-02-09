# -*- coding: utf-8 -*-
def preprocess_general(lyric, delimiter):
    new_lyric=[]
    empty_style=''
    for line in lyric:
        split_line=line.split(delimiter,1)
        #if no delimiter, we use the emptystyle
        if len(split_line)==1:
            split_line=[empty_style,split_line[0]]

        #search for meta data tags, and set the emptystyle to
        #that tag so that constructive lines without additional tags
        #will be intepreted as having the previous tag
        if not split_line[0].lower() in ["titel", "melodi", "arr", "författare", "text", "medv"]:
            new_lyric.append(line)
            
        empty_style=split_line[0]
    return new_lyric

def preprocess_ass(lyric,delimiter):
    return preprocess_general(lyric, delimiter)

def preprocess_inputsong(lyric,delimiter):
    # does exactly the same as the general preprocessor actually.
    return preprocess_general(lyric, delimiter)
