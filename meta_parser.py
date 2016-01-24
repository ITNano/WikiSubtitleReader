# -*- coding: utf-8 -*-
#Python function that finds tagged metadata in list of lines of text

#acceptable metadata tags:
#Titel: We Rickroll the audience
#Melodi: Never Gonna Give You Up -- Rick Astley
#Arr: Torbjörn X
#Författare: XX, XXXX, XXXXX
#Medv: X, XX, XXX


class kuplett_meta:
    titel=''
    melodi=''
    arr=''
    forf=''
    medv=''



def get_metadata(lyric,delimiter):
    meta=kuplett_meta()
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
            meta.titel=meta.titel+split_line[1].strip()
            empty_style="titel"
        elif split_line[0].lower()=="melodi":
            meta.melodi=meta.melodi+split_line[1].strip()
            empty_style="melodi"
        elif split_line[0].lower()=="arr":
            meta.arr=meta.arr+split_line[1].strip()
            empty_style="arr"
        elif split_line[0].lower()==u"författare":
            meta.forf=meta.forf+split_line[1].strip()
            empty_style=u"författare"
        elif split_line[0].lower()==u"medv":
            meta.medv=meta.medv+split_line[1].strip()
            empty_style=u"medv"
        else: 
            empty_style=split_line[0].lower()
    return meta

