# -*- coding: utf-8 -*-

from wiki_to_text import wiki_to_text

from os import listdir
import codecs
import sys

def read_texts(dir):
    lyrics = [] #returns this
    filenames = [dir + "/" + fname for fname in sorted(listdir(dir))]
    # print(filenames)
    for filename in filenames:
        file = codecs.open(filename, 'r', 'utf-8')
        lyric = [line.rstrip('\n') for line in file]
        lyrics.append(lyric)
    return lyrics

if __name__ == "__main__":
    lyrics1 = read_texts("texts")
    if len(sys.argv)<4:
        print("Need 3 arguments.")
        print("Usage:")
        print("get_and_parse_kuplett.py USERNAME PASSWORD OUTFILE_NAME")
        sys.exit(3)
    #if os.path.exists(sys.argv[3]):
     #   print("File '"+sys.argv[3]+"' already exists. Delete or rename it and try again.")
      #  sys.exit(1)
    lyrics2 = wiki_to_text(sys.argv[1], sys.argv[2], sys.argv[3],sourcefile="data_2017.txt")

    # for all lines in lyric in lyrics, assert that the two methods yield the same
    for ly1,ly2 in zip(lyrics1,lyrics2):
        for l1,l2 in zip(ly1,ly2):
            print(repr(l1))
            print(repr(l2))
            assert(l1 == l2)
