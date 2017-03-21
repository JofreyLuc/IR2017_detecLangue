#!/usr/bin/env python3
#Script pour convertir tous les fichiers du dossier mfcc en un gros fichier csv
#python3 convertAllToCsv.py mfcc/ data.csv

from subprocess import check_call #Pour appeler les scripts de conversion
import sys                        #Pour les arguments + l'exécutable python
from glob import glob             #Pour lister les fichiers
from os import path, remove       #Pour supprimer le fichier si il existe déjà

def convertAllToCsv(mfccFolderName, csvFileName) :

    AFFICHAGE = False #Activer l'affichage pendant la conversion

    if path.isfile(csvFileName) : remove(csvFileName)
    
    for arabicFile in glob(mfccFolderName + "arabic/*.mfcc") :
        check_call([sys.executable, "convertMfccToCsv.py", arabicFile, str(0), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + arabicFile)

    for englishFile in glob(mfccFolderName + "english/*.mfcc") :
        check_call([sys.executable, "convertMfccToCsv.py", englishFile, str(1), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + englishFile)

    for frenchFile in glob(mfccFolderName + "french/*.mfcc") :
        check_call([sys.executable, "convertMfccToCsv.py", frenchFile, str(2), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + frenchFile)

    for germanFile in glob(mfccFolderName + "german/*.mfcc") :
        check_call([sys.executable, "convertMfccToCsv.py", germanFile, str(3), csvFileName], shell=False)
        if AFFICHAGE : print("Traité : " + germanFile)
    
if __name__ == '__main__':
    convertAllToCsv(sys.argv[1], sys.argv[2])
