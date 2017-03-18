#!/usr/bin/env python3
#Script pour faire la conversion du corpus en .mfcc
#python3 convertAll.py

from subprocess import check_call
from os import path, makedirs
import sys

def convertAll() :

    if not path.exists("../mfcc") : makedirs("../mfcc")
    if not path.exists("../mfcc/arabic") : makedirs("../mfcc/arabic")
    if not path.exists("../mfcc/english") : makedirs("../mfcc/english")
    if not path.exists("../mfcc/french") : makedirs("../mfcc/french")
    if not path.exists("../mfcc/german") : makedirs("../mfcc/german")

    check_call([sys.executable, "convertFolder.py", "../corpus/arabic/", "../transcripts/arabic/", "../mfcc/arabic/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolder.py", "../corpus/english/", "../transcripts/english/", "../mfcc/english/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolder.py", "../corpus/french/", "../transcripts/french/", "../mfcc/french/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolder.py", "../corpus/german/", "../transcripts/german/", "../mfcc/german/", "confightk"], shell=False)

if __name__ == '__main__':
    convertAll()
