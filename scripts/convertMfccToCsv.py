#!/usr/bin/env python3
#Script pour convertir un fichier mfcc dans un fichier csv en l'étiquettant
#python3 convertMfccToCsv.py fichier.mfcc codeLangue out.csv

import sys,os
from subprocess import call
from platform import system             #Pour connaitre l'environnement d'execution
import csv
from os import remove                   #Pour supprimer des fichiers
from os import path                                             # Pour couper l'extension de fichier
import numpy as np
import h5py

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
    currentLine = ifile.readline()
    
    mfcc = []
    #Pour tout le fichier
    while (currentLine != '') :
        #Si on est sur une ligne de données
        if (not currentLine.startswith('-')) :
            #On lit la ligne suivante, on ajoute la langue et on écrit dans le csv
            currentLine += ifile.readline()
            mfccRow = currentLine.split()[1:]
            mfccRow.append(language)
            mfcc.append(mfccRow)
   
        currentLine = ifile.readline()
    
    ifile.close()
    remove(tmpFile)
    
    npMfcc = np.asarray(mfcc)
    #création du conteneur HDF5
    hdf5Out = h5py.File("train.hdf5", "w") 
    #on crée 1 dataset hdf5 pour ce fichier mfcc 
    fileName = path.splitext(path.basename(mfccFileName))[0] #Nom du fichier sans extension
    hdf5Out.create_dataset(fileName, data=npMfcc)
    hdf5Out.close()
    
if __name__ == '__main__':
    convertMfccToCsv(sys.argv[1], sys.argv[2], sys.argv[3])
