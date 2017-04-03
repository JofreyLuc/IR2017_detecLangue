#!/usr/bin/env python3

# Script qui permet de couper au début ou à la fin d'un fichier audio (.wav)
# un silence ou un passage musical à partir d'un fichier de transcription correspondant.
# Supporte uniquement l'extension audio .wav.
# Supporte les formats de transcriptions suivants :
#   - .stm
#   - .mlfmanu

# Usage : python cutAudioFile.py audio.wav transcriptFile.* audio_trimmed.wav
import sys
from os import path                                             # Pour couper l'extension de fichier
from subprocess import check_output, CalledProcessError, STDOUT # Pour lancer sox
# Pour parser les arguments
from argparse import ArgumentParser, RawTextHelpFormatter, ArgumentTypeError
import sys
import utils

# Cherche le début et la fin de la coupe dans le fichier de transcription.
# Retourne les temps de début et de fin de la coupe en secondes.
# Format stm.
def searchBeginAndEndStm(transFileName):
    fileName = path.splitext(path.basename(transFileName))[0] # Nom du stm sans extension

    # On ouvre le fichier avec le bon encodage si celui-ci est précisé
    if (path.isfile(path.dirname(transFileName) + "/encoding.txt")):
        e = open(path.dirname(transFileName) + "/encoding.txt", 'r')
        encod = e.readline()
        f = open(transFileName, 'r', encoding=encod)
        e.close()
    else:
        f = open(transFileName, 'r')

    #Tant qu'on a pas une ligne de transcription (commencant par le nom de fichier) on lit en avancant
    currentLine = f.readline()
    while (currentLine.split()[0] != fileName):
        currentLine = f.readline()

    #Si la première ligne est un silence/musique, on prend comme début le timestamp de fin, sinon le timestamp de début
    if (currentLine.split()[2] == "inter_segment_gap"):
        debut = float(currentLine.split()[4])
    else:
        debut = float(currentLine.split()[3])
            
    #On va jusqu'à la fin du fichier en conservant la dernière ligne "correcte"
    nextLine = f.readline()
    while (nextLine != ''):
        if (nextLine.split()[0] == fileName and nextLine.split()[2] != "inter_segment_gap"):
            currentLine = nextLine
        nextLine = f.readline()

    #On prend la fin de la dernière phrase
    fin = float(currentLine.split()[4])     
    
    f.close()

    return (debut, fin)

# Cherche le début et la fin de la coupe dans le fichier de transcription.
# Retourne les temps de début et de fin de la coupe en secondes.
# Format mlfmanu.
def searchBeginAndEndMlfmanu(transFileName):
    fileName = path.splitext(path.basename(transFileName))[0] #Nom du fichier sans extension
    
    f = open(transFileName, 'r')
    currentLine = f.readline()
    # On lit le fichier ligne par ligne tant qu'on a pas atteint une ligne non vide,
    # qui n'est pas un commentaire ou qui n'est pas un silence.
    while (currentLine[0] == "#" or currentLine[0] == "\"" or currentLine.split()[2] == "sil"):
        currentLine = f.readline()

    debut = float(currentLine.split()[0]) / 10000000; #Conversion en secondes

    nextLine = f.readline()
    # On lit ligne par ligne tant qu'on a pas atteint la dernière ligne (ligne de silence exclus)
    while (nextLine[0] != '.'):
        if (nextLine.split()[2] != "sil"):
            currentLine = nextLine
        nextLine = f.readline()
            
    fin = float(currentLine.split()[1]) / 10000000; #Conversion en secondes
    
    f.close()
    
    return (debut, fin)

# Coupe le fichier audio de cutBegin jusqu'à cutEnd (en secondes).
def cutAudioFile(audioFileName, cutFileName, cutBegin, cutEnd):
    duration = cutEnd - cutBegin
    try:
        check_output("sox " + audioFileName + " " + cutFileName + " trim " + str(cutBegin) + " " + str(duration), shell = True, stderr=STDOUT)
    except CalledProcessError as exc:                                                                                          
        utils.eprintCalledProcessError(exc, "à SOX")
        sys.exit(1)

def main(audioFileName, transFileName, outputFileName, beginningTime=None, endTime=None):
    extension = path.splitext(transFileName)[1]
    if (extension == ".stm"):
        (debut, fin) = searchBeginAndEndStm(transFileName)
    elif (extension == ".mlfmanu"):
        (debut, fin) = searchBeginAndEndMlfmanu(transFileName)
        
    # On prend les temps "les plus limitants"
    if (beginningTime is not None and beginningTime > debut):
        debut = beginningTime
    if (endTime is not None and endTime < fin):
        fin = endTime

    cutAudioFile(audioFileName, outputFileName, debut, fin) # On coupe le fichier audio

def parseArgs():
    parser = ArgumentParser(description="Programme python permettant de couper un fichier audio en retirant un silence ou un passage musical au début ou à la fin du fichier à l'aide de son fichier de transcription.\n"
    "Si les options -beginning ou -end sont spécifiées, le temps le plus limitant entre le contenu de la transcription et l'option sera utilisé.", formatter_class=RawTextHelpFormatter)
    parser.add_argument("audioFileName", metavar="audioFile",
                        help="fichier audio (extension wav uniquement).",
                        type=utils.isValidFile)
    parser.add_argument("transFileName", metavar="transcriptFile",
                        help="fichier de transcription (extensions stm et mlfmanu supportées).",
                        type=utils.isValidTranscriptFile)
    parser.add_argument("outputFileName", metavar="outputFile",
                        help="nom du fichier de sortie (coupé).")						
    parser.add_argument("-b", "--beginning", dest="beginningTime", required=False,
                       help="le temps de début de la coupe.", metavar="beginningTime",
                       type=utils.isPositiveNumber)
    parser.add_argument("-e", "--end", dest="endTime", required=False,
                   help="le temps de fin de la coupe.", metavar="endTime",
                   type=utils.isPositiveNumber)
    
    args = parser.parse_args()
    
    return (args.audioFileName, args.transFileName, args.outputFileName, args.beginningTime, args.endTime)
    
if __name__ == '__main__':
    args = parseArgs()  # Parse les arguments
    main(*args)         # Unpack le tuple et passe les éléments en paramétre du main 
