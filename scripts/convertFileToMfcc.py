#!/usr/bin/env python3
#Script pour transformer un fichier audio en .mfcc
#python3 convertFileToMfcc.py audio.* transcript.stm resultat.mfcc confightk

from os import path                     #Pour couper l'extension de fichier
from os import remove                   #Pour supprimer des fichiers
import sys                              #Pour récuperer les arguments du programme
from subprocess import call, check_call #Pour lancer sox, htk et les scripts python
from platform import system             #Pour connaitre l'environnement d'exécution

def convertFileToMfcc(audioFileName, transFileName, mfccFileName, configFile) :
    
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
        check_call([sys.executable, "cutStm.py", audioFileName, transFileName, cutFileName], shell=False)
    elif (path.splitext(transFileName)[1] == ".mlfmanu") :
        check_call([sys.executable, "cutMlfmanu.py", audioFileName, transFileName, cutFileName], shell=False)
    else :
        sys.exit("Format de transcript inconnu")

    #Génération des mfcc
    if (linux) :
	    hCopyCall = "./HCopy"
    elif (windows) :
	    hCopyCall = "HCopy"
    call(hCopyCall + " -C " + configFile + " " + cutFileName + " " + mfccFileName, shell = True) 

    #Suppression des fichiers de transition
    if (hasBeenConverted) :
        remove(wavFileName)
    remove(cutFileName)


if __name__ == '__main__':
    convertFileToMfcc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])

