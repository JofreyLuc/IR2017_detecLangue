#!/usr/bin/env python3
#Script pour couper le début et la fin de non-parole des fichiers stm
#python3 cutStm.py audio.wav transcript.stm audio_trimmed.wav

from os import path         #Pour couper l'extension de fichier
import sys                  #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer sox
import argparse				#Pour parser les arguments

# Vérifie si la chaîne de caractères passées en paramètres correspond bien à un fichier existant 
def is_valid_file(filename):
    if not path.isfile(filename):
        raise argparse.ArgumentTypeError("%s n'existe pas ou n'est pas un fichier valide." % filename)
    return filename  # retourne le nom du fichier

# Vérifie si la valeur passée en paramètre est bien un nombre positif
def is_positive_number(string):
    try :
        value = float(string)
        if value < 0 :
            raise argparse.ArgumentTypeError("%s n'est pas un nombre positif." % string)
    except ValueError :
        raise argparse.ArgumentTypeError("%s n'est pas un nombre positif." % string)
    return value

def cutStm(audioFileName, transFileName, cutFileName, beginningTime):

    transName = path.splitext(path.basename(transFileName))[0] #Nom du stm sans extension

    #On ouvre le fichier, tant qu'on a pas une ligne de transcription (commencant par le nom de fichier) on lit en avancant
    if (path.isfile(path.splitext(audioFileName)[0] + ".encoding")) :
        #Lire le fichier avec le bon encodage
	    print("lol")
    else :
        f = open(transFileName, 'r')
    currentLine = f.readline()
    while (currentLine.split()[0] != transName) :
        currentLine = f.readline()

    #Si le temps de début de la coupe est précisé, on ne regarde pas le début dans le fichier de transcription
    if beginningTime is None :
        #Si la première ligne est un silence/musique, on prend comme début le timestamp de fin; sinon le timestamp de début
        if (currentLine.split()[2] == "inter_segment_gap") :
            debut = currentLine.split()[4]
        else :
            debut = currentLine.split()[3]
    else :
        debut = beginningTime
            
    #On va jusqu'à la fin du fichier en conservant la dernière ligne "correcte"
    nextLine = f.readline()
    while (nextLine != '') :
        if (nextLine.split()[0] == transName and nextLine.split()[2] != "inter_segment_gap") :
            currentLine = nextLine
        nextLine = f.readline()

    #On prend la fin de la dernière phrase et on calcule la durée totale à conserver
    fin = currentLine.split()[4]        
    duree = float(fin) - float(debut)
    
    f.close()

    #On coupe le fichier avec sox
    call("sox " + audioFileName + " " + cutFileName + " trim " + str(debut) + " " + str(duree), shell = True)

if __name__ == '__main__':
# On parse les arguments
    parser = argparse.ArgumentParser(description="Programme python permettant de couper un fichier audio a partir de son fichier de transcription.")
    parser.add_argument("audioFileName", metavar="audioFile",
                        help="fichier audio.",
                        type=is_valid_file)
    parser.add_argument("transcriptFileName", metavar="transcriptFile",
                        help="fichier de transcription.",
                        type=is_valid_file)
    parser.add_argument("outputFileName", metavar="outputFile",
                        help="nom du fichier coupe (en sortie).")						
    parser.add_argument("-b", "--beginning", dest="beginningTime", required=False,
                       help="le temps de début de la coupe", metavar="beginningTime",
                       type=is_positive_number)
    
    args = parser.parse_args()
    cutStm(args.audioFileName, args.transcriptFileName, args.outputFileName, args.beginningTime)
