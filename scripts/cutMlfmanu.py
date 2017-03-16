#!/usr/bin/env python3
#Script pour couper le début et la fin de non-parole des fichiers mlfmanu
#python3 cutMlfmanu.py audio.wav transcript.stm audio_trimmed.wav

from os import path #Pour couper l'extension de fichier
import sys #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer le bash sox


def cut(audioFileName, fileNameExt, cutFileName):

    fileName = path.splitext(path.basename(fileNameExt))[0] #Nom du mlfmanu sans extension

    f = open(fileNameExt, 'r')
    currentLine = f.readline()
    while (currentLine[0] is "#" or currentLine[0] is "\"" or currentLine.split()[2] is "sil") :
        currentLine = f.readline()

    debut = float(currentLine.split()[0]) / 10000000;	#Conversion en secondes

    nextLine = f.readline()
    while (not nextLine[0] is '.') :
	    if (nextLine.split()[2] != "sil") :
		    currentLine = nextLine
	    nextLine = f.readline()
    
    fin = float(currentLine.split()[1]) / 10000000;		#Conversion en secondes

    duree = fin - debut
    
    f.close()

    #On appelle le script bash qui va couper le fichier avec sox
    call("sox " + audioFileName + " " + cutFileName + " trim " + str(debut) + " " + str(duree), shell = True)

cut(sys.argv[1], sys.argv[2], sys.argv[3])
