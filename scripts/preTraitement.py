#!/usr/bin/env python3
#Script effectuant le prétraitement des données
#python3 preTraitement.py

from subprocess import check_call #Pour appeler les scripts de conversion
import sys                        #Pour les arguments + l'exécutable python

def preTraitement() :

    AFFICHAGE = True #Activer l'affichage pendant la conversion

    if AFFICHAGE : print("Conversion de l'audio en mfcc..")
    check_call([sys.executable, "convertAllToMfcc.py"], shell=False)

    if AFFICHAGE : print("Conversion des mfcc en hdf5..")
    check_call([sys.executable, "convertAllToHdf5.py", "../mfcc/", "data.hdf5"], shell=False)

if __name__ == '__main__':
    preTraitement()

    
