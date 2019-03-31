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
        #
        #NOTE: Any meta word that is added here must be added in preprocess.py as well
        if split_line[0].lower() in ["titel"]:
            meta.titel=meta.titel+split_line[1].strip()
            empty_style="titel"
        elif split_line[0].lower() in ["melodi", "mel"]:
            meta.melodi=meta.melodi+split_line[1].strip()
            empty_style="melodi"
        elif split_line[0].lower() in ["arr","arrare","arrangemang"]:
            meta.arr=meta.arr+split_line[1].strip()
            empty_style="arr"
        elif split_line[0].lower() in ["författare", "text"]:
            meta.forf=meta.forf+split_line[1].strip()
            empty_style=u"författare"
        elif split_line[0].lower() in ["medv","medverkande","karaktärer","sjungs av"]:
            meta.medv=meta.medv+split_line[1].strip()
            empty_style=u"medv"
        else: 
            empty_style=split_line[0].lower()
    return meta

