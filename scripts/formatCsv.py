#!/usr/bin/env python3

from subprocess import check_call
import sys
from glob import glob

def formatCsv(mfccFolderName, csvFileName) :

    AFFICHAGE = False

    for arabicFile in glob(mfccFolderName + "arabic/*.mfcc") :
        check_call([sys.executable, "convertMfccToCSV.py", arabicFile, str(0), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + arabicFile)

    for englishFile in glob(mfccFolderName + "english/*.mfcc") :
        check_call([sys.executable, "convertMfccToCSV.py", englishFile, str(1), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + englishFile)

    for frenchFile in glob(mfccFolderName + "french/*.mfcc") :
        check_call([sys.executable, "convertMfccToCSV.py", frenchFile, str(2), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + frenchFile)

    for germanFile in glob(mfccFolderName + "german/*.mfcc") :
        check_call([sys.executable, "convertMfccToCSV.py", germanFile, str(3), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + germanFile)
    
if __name__ == '__main__':
    formatCsv(sys.argv[1], sys.argv[2])
