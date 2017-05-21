#!/usr/bin/env python3
#Script pour faire la conversion du corpus en .mfcc
#python3 convertAllToMfcc.py

from subprocess import check_call #Pour appeler les scripts de conversion
from os import path, makedirs     #Pour créer les dossiers
import sys                        #Pour avoir l'exécutable python

def convertAllToMfcc() :

    #Arborescence par défaut : on crée les mfcc un niveau au-dessus
    if not path.exists("../mfcc") : makedirs("../mfcc")
    if not path.exists("../mfcc/arabic") : makedirs("../mfcc/arabic")
    if not path.exists("../mfcc/english") : makedirs("../mfcc/english")
    if not path.exists("../mfcc/french") : makedirs("../mfcc/french")
    if not path.exists("../mfcc/german") : makedirs("../mfcc/german")

    #On appelle le script de conversion sur les fichiers du corpus
    check_call([sys.executable, "convertFolderToMfcc.py", "../train/corpus/arabic/", "../train/transcripts/arabic/", "../mfcc/arabic/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfcc.py", "../train/corpus/english/", "../train/transcripts/english/", "../mfcc/english/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfcc.py", "../train/corpus/french/", "../train/transcripts/french/", "../mfcc/french/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfcc.py", "../train/corpus/german/", "../train/transcripts/german/", "../mfcc/german/", "confightk"], shell=False)

if __name__ == '__main__':
    convertAllToMfcc()
