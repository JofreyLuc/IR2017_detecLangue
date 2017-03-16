#!/usr/bin/env python3
#Script pour transformer un fichier audio en .mfcc
#python3 audio.* transcript.stm confightk

import cutStm               #Script de découpe des stm
from os import path         #Pour couper l'extension de fichier
from os import remove       #Pour supprimer des fichiers
import sys                  #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer sox et htk
from platform import system #Pour connaitre l'environnement d'execution

hasBeenConverted = False    #Indique si on a du convertir le fichier en .wav

#Gestion de l'OS
linux=False
windows=False
if (system() == "Linux") :
    linux = True
elif (system() == 'Windows') :
    windows = True
else :
    sys.exit("OS inconnu")

def convertToMfcc(audioFileName, transFileName, configFile) :
    
    audioName = path.splitext(path.basename(audioFileName))[0] #Nom du fichier audio sans extension
    
    #Conversion en wav si besoin
    if (not(path.splitext(audioFileName)[1] is ".wav")) :
        wavFileName = audioName + ".wav"
        call("sox " + audioFileName + " " + wavFileName, shell = True)
        audioName = wavFileName
        hasBeenConverted = True

    #Coupe de l'audio
    cutFileName = path.splitext(audioName)[0] + "_trimmed.wav"
    cutStm.cutStm(audioName, transFileName, cutFileName)

    #Génération des mfcc
    mfcFileName = path.splitext(audioName)[0] + ".mfcc"
    call("./HCopy -C " + configFile + " " + cutFileName + " " + mfcFileName, shell = True) 

    #Suppression des fichiers de transition
    if (hasBeenConverted) :
        remove(wavFileName)
    remove(cutFileName)


if __name__ == '__main__':
    convertToMfcc(sys.argv[1], sys.argv[2], sys.argv[3])

