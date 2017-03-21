#!/usr/bin/env python3
#Script effectuant le prétraitement des données
#python3 preTraitement.py

from subprocess import check_call #Pour appeler les scripts de conversion
import sys                        #Pour les arguments + l'exécutable python

def preTraitement() :

    AFFICHAGE = True #Activer l'affichage pendant la conversion

    if AFFICHAGE : print("Conversion de l'audio en mfcc..")
    check_call([sys.executable, "convertAllToMfcc.py"], shell=False)

    if AFFICHAGE : print("Conversion des mfcc en csv..")
    check_call([sys.executable, "convertAllToCsv.py", "../mfcc/", "data.csv"], shell=False)

if __name__ == '__main__':
    preTraitement()

    
