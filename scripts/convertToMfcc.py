#!/usr/bin/env python3
#Script pour transformer un fichier audio en .mfcc
#python3 audio.* transcript.stm confightk

import cutStm               #Script de découpe des stm
from os import path         #Pour couper l'extension de fichier
import sys                  #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer sox et htk
from platform import system #Pour connaitre l'environnement d'execution

audioFileName = sys.argv[1] #Fichier audio
transFileName = sys.argv[2] #Fichier de transcription
configFile = sys.argv[3]    #Fichier de configuration HTK

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

#Conversion en wav si besoin
if (path.splitext(audioFileName)[1] != ".wav") :
    wavFileName = path.splitext(audioFileName)[0] + ".wav"
    call("sox " + audioFileName + " " + wavFileName, shell = True)
    audioFileName = wavFileName
    hasBeenConverted = True
    

#Coupe de l'audio
cutFileName = path.splitext(audioFileName)[0] + "_trimmed.wav"
cutStm.cut(audioFileName, transFileName, cutFileName)

#Génération des mfcc
mfcFileName = path.splitext(audioFileName)[0] + ".mfcc"
call("./HCopy -C " + configFile + " " + cutFileName + " " + mfcFileName, shell = True) 

#Suppression des fichiers de transition

if (linux) :
    if (hasBeenConverted) :
        call("rm " + wavFileName, shell = True)
    call("rm " + cutFileName, shell = True)
#elif (windows) :
    #whatevs
