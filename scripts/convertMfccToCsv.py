#!/usr/bin/env python3
#Script pour convertir un fichier mfcc dans un fichier csv en l'étiquettant
#python3 convertMfccToCsv.py fichier.mfcc codeLangue out.csv

import sys,os
from subprocess import call
from platform import system             #Pour connaitre l'environnement d'execution
import csv
from os import remove                   #Pour supprimer des fichiers

def convertMfccToCsv(mfccFileName, language, outputFile) :
    
    #Gestion de l'OS
    linux=False
    windows=False
    if (system() == "Linux") :
        linux = True
    elif (system() == "Windows") :
        windows = True
    else :
        sys.exit("OS inconnu")

        
    tmpFile = "HListTmp" #Fichier texte temporaire généré par HList
        
    #Génération des mfcc
    if (linux) :
        hListCall = "./HList"
    elif (windows) :
        hListCall = "HList"
    call(hListCall + " " + mfccFileName + " >> " + tmpFile, shell = True)        

    ifile = open(tmpFile, 'r') #Fichier d'entrée
    ofile = open(outputFile, 'a', newline="") #Fichier de sortie (crée si non existant)
    wr = csv.writer(ofile) #Formatteur csv
    currentLine = ifile.readline()

    #Pour tout le fichier
    while (currentLine != '') :
        #Si on est sur une ligne de données
        if (not currentLine.startswith('-')) :
            #On lit la ligne suivante, on ajoute la langue et on écrit dans le csv
            currentLine += ifile.readline()
            mfcc = currentLine.split()[1:]
            mfcc.append(language)
            wr.writerow(mfcc)
   
        currentLine = ifile.readline()

    ifile.close()
    ofile.close()  
    remove(tmpFile)

if __name__ == '__main__':
    convertMfccToCsv(sys.argv[1], sys.argv[2], sys.argv[3])
