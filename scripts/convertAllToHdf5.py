#!/usr/bin/env python3
#Script pour convertir tous les fichiers du dossier mfcc en un gros fichier hdf5
#python3 convertAllToHdf5.py mfcc/ data.hdf5

from subprocess import check_call #Pour appeler les scripts de conversion
import sys                        #Pour les arguments + l'exécutable python
from glob import glob             #Pour lister les fichiers
from os import path, remove       #Pour supprimer le fichier si il existe déjà

def convertAllToHdf5(mfccFolderName, hdf5FileName) :

    AFFICHAGE = True #Activer l'affichage pendant la conversion

    if path.isfile(hdf5FileName) : remove(hdf5FileName)
    
    for arabicFile in glob(mfccFolderName + "arabic/*.mfcc") :
        check_call([sys.executable, "convertMfccToHdf5.py", arabicFile, str(0), hdf5FileName], shell=False)
        if AFFICHAGE : print("Traité : " + arabicFile)

    for englishFile in glob(mfccFolderName + "english/*.mfcc") :
        check_call([sys.executable, "convertMfccToHdf5.py", englishFile, str(1), hdf5FileName], shell=False)
        if AFFICHAGE : print("Traité : " + englishFile)

    for frenchFile in glob(mfccFolderName + "french/*.mfcc") :
        check_call([sys.executable, "convertMfccToHdf5.py", frenchFile, str(2), hdf5FileName], shell=False)
        if AFFICHAGE : print("Traité : " + frenchFile)

    for germanFile in glob(mfccFolderName + "german/*.mfcc") :
        check_call([sys.executable, "convertMfccToHdf5.py", germanFile, str(3), hdf5FileName], shell=False)
        if AFFICHAGE : print("Traité : " + germanFile)
    
if __name__ == '__main__':
    convertAllToHdf5(sys.argv[1], sys.argv[2])
