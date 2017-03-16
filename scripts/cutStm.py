#!/usr/bin/env python3
#Script pour couper le début et la fin de non-parole des fichiers stm
#python3 cutStm.py audio.wav transcript.stm audio_trimmed.wav

from os import path         #Pour couper l'extension de fichier
import sys                  #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer sox


def cut(audioFileName, transFileName, cutFileName):

    name = path.splitext(path.basename(transFileName))[0] #Nom du stm sans extension

    #On ouvre le fichier, tant qu'on a pas une ligne de transcription (commencant par le nom de fichier) on lit en avancant
    f = open(transFileName, 'r')
    currentLine = f.readline()
    while (currentLine.split()[0] != name) :
        currentLine = f.readline()

    #Si la première ligne est un silence/musique, on prend comme début le timestamp de fin; sinon le timestamp de début
    if (currentLine.split()[2] == "inter_segment_gap") :
        debut = currentLine.split()[4]
    else :
        debut = currentLine.split()[3]

    #On va jusqu'à la fin du fichier en conservant la dernière ligne "correcte"
    nextLine = f.readline()
    while (nextLine != '') :
        if (nextLine.split()[0] == name and nextLine.split()[2] != "inter_segment_gap") :
            currentLine = nextLine
        nextLine = f.readline()

    #On prend la fin de la dernière phrase et on calcule la durée totale à conserver
    fin = currentLine.split()[4]        
    duree = float(fin) - float(debut)
    
    f.close()

    #On coupe le fichier avec sox
    call("sox " + audioFileName + " " + cutFileName + " trim " + str(debut) + " " + str(duree), shell = True)

if __name__ == '__main__':
    cut(sys.argv[1], sys.argv[2], sys.argv[3])
