# -*- coding: utf-8 -*-
def preprocess_ass(lyric,delimiter):
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
        if split_line[0].lower()=="titel":
            empty_style="titel"
        elif split_line[0].lower()=="melodi":
            empty_style="melodi"
        elif split_line[0].lower()=="arr":
            empty_style="arr"
        elif split_line[0].lower()==u"författare":
            empty_style=u"författare"
        elif split_line[0].lower()==u"medv":
            empty_style=u"medv"
        else:
            new_lyric.append(line)
        empty_style=split_line[0]
    return new_lyric

def preprocess_inputsong(lyric,delimiter):
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
        if split_line[0].lower()=="titel":
            empty_style="titel"
        elif split_line[0].lower()=="melodi":
            empty_style="melodi"
        elif split_line[0].lower()=="arr":
            empty_style="arr"
        elif split_line[0].lower()==u"författare":
            empty_style=u"författare"
        elif split_line[0].lower()=="kommentar":
            empty_style="kommentar"
        elif split_line[0].lower()==u"medv":
            empty_style=u"medv"
        else:
            new_lyric.append(line)
            empty_style=split_line[0]
    return new_lyric
