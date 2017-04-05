#!/usr/bin/env python3
#Script pour faire la conversion du corpus de dev/test en .mfcc
#python3 convertAllToMfcc.py

from subprocess import check_call #Pour appeler les scripts de conversion
from os import path, makedirs     #Pour créer les dossiers
import sys                        #Pour avoir l'exécutable python

def convertAllToMfcc() :

    #DEV
    
    #Arborescence par défaut : on crée les mfcc un niveau au-dessus
    if not path.exists("../mfccdev") : makedirs("../mfccdev")
    if not path.exists("../mfccdev/arabic") : makedirs("../mfccdev/arabic")
    if not path.exists("../mfccdev/english") : makedirs("../mfccdev/english")
    if not path.exists("../mfccdev/french") : makedirs("../mfccdev/french")
    if not path.exists("../mfccdev/german") : makedirs("../mfccdev/german")

    #On appelle le script de conversion sur les fichiers du corpus
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../dev/corpus/arabic/", "../mfccdev/arabic/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../dev/corpus/english/", "../mfccdev/english/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../dev/corpus/french/", "../mfccdev/french/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../dev/corpus/german/", "../mfccdev/german/", "confightk"], shell=False)


    #TEST
    
    if not path.exists("../mfcctest") : makedirs("../mfcctest")
    if not path.exists("../mfcctest/arabic") : makedirs("../mfcctest/arabic")
    if not path.exists("../mfcctest/english") : makedirs("../mfcctest/english")
    if not path.exists("../mfcctest/french") : makedirs("../mfcctest/french")
    if not path.exists("../mfcctest/german") : makedirs("../mfcctest/german")

    #On appelle le script de conversion sur les fichiers du corpus
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../test/corpus/arabic/", "../mfcctest/arabic/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../test/corpus/english/", "../mfcctest/english/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../test/corpus/french/", "../mfcctest/french/", "confightk"], shell=False)
    check_call([sys.executable, "convertFolderToMfccWITHOUTTRANS.py", "../test/corpus/german/", "../mfcctest/german/", "confightk"], shell=False)

    
if __name__ == '__main__':
    convertAllToMfcc()
