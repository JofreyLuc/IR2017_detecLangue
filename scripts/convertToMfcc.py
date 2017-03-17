#!/usr/bin/env python3
#Script pour transformer un fichier audio en .mfcc
#python3 convertToMfcc.py audio.* transcript.stm confightk

import cutStm               #Script de découpe des stm
import cutMlfmanu           #Script de découpe des mlfmanu
from os import path         #Pour couper l'extension de fichier
from os import remove       #Pour supprimer des fichiers
import sys                  #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer sox et htk
from platform import system #Pour connaitre l'environnement d'execution


def convertToMfcc(audioFileName, transFileName, configFile) :
    
    #Gestion de l'OS
    linux=False
    windows=False
    if (system() == "Linux") :
        linux = True
    elif (system() == "Windows") :
        windows = True
    else :
        sys.exit("OS inconnu")

    hasBeenConverted = False    #Indique si on a du convertir le fichier en .wav
        
    audioName = path.splitext(path.basename(audioFileName))[0] #Nom du fichier audio sans extension
    
    #Conversion en wav si besoin
    if (path.splitext(audioFileName)[1] != ".wav") :
        wavFileName = audioName + ".wav"
        call("sox " + audioFileName + " " + wavFileName, shell = True)
        audioName = wavFileName
        hasBeenConverted = True

    #Coupe de l'audio
    cutFileName = path.splitext(audioName)[0] + "_trimmed.wav"
    if (path.splitext(transFileName)[1] == ".stm") :
        cutStm.cutStm(audioFileName, transFileName, cutFileName)
    elif (path.splitext(transFileName)[1] == ".mlfmanu") :
        cutMlfmanu.cutMlfmanu(audioFileName, transFileName, cutFileName)
    else :
        sys.exit("Format de transcript inconnu")

    #Génération des mfcc
    mfcFileName = path.splitext(audioName)[0] + ".mfcc"
    if (linux) :
	    hCopyCall = "./HCopy"
    elif (windows) :
	    hCopyCall = "HCopy"
    call(hCopyCall + " -C " + configFile + " " + cutFileName + " " + mfcFileName, shell = True) 

    #Suppression des fichiers de transition
    if (hasBeenConverted) :
        remove(wavFileName)
    remove(cutFileName)


if __name__ == '__main__':
    convertToMfcc(sys.argv[1], sys.argv[2], sys.argv[3])

