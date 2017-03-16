#!/usr/bin/env python3
#Script pour couper le début et la fin de non-parole des fichiers stm
#python3 cutStm.py audio.wav transcript.stm audio_trimmed.wav

from os import path #Pour couper l'extension de fichier
import sys #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer le bash sox


def cut(audioFileName, fileNameExt, cutFileName):

    fileName = path.splitext(fileNameExt)[0] #Nom du stm sans extension

    f = open(fileNameExt, 'r')
    currentLine = f.readline()
    while (currentLine.split()[0] != fileName) :
        currentLine = f.readline()

    if (currentLine.split()[2] == "inter_segment_gap") :
        debut = currentLine.split()[4]
    else :
        debut = currentLine.split()[3]

    nextLine = f.readline()
    while (nextLine != '') :
        if (nextLine.split()[0] == fileName and nextLine.split()[2] != "inter_segment_gap") :
            currentLine = nextLine
        nextLine = f.readline()

    fin = currentLine.split()[4]
        
    duree = float(fin) - float(debut)
    
    f.close()

    #On appelle le script bash qui va couper le fichier avec sox
    call("sox " + audioFileName + " " + cutFileName + " trim " + str(debut) + " " + str(duree), shell = True)

cut(sys.argv[1], sys.argv[2], sys.argv[3])
