#!/usr/bin/env python3
#Script pour transformer un dossier de fichiers audio (et leur transcription) en fichiers .mfcc
#python3 convertFolder.py audio/ transcript/ dest/ confightk

from subprocess import check_call #Pour appeller le script de conversion
from os import path               #Pour récupérer les noms de fichier/extensions
import sys                        #Pour les arguments du programme
from glob import glob             #Pour lister des fichiers

def convertFolder(audioFolderName, transFolderName, destFolderName, configFile) :

    AFFICHAGE = True
    AUDIO_TYPES = [".wav", ".WAV", ".sph", ".SPH"]
    TRANSCRIPT_TYPES = [".stm", ".STM", ".mlfmanu", ".MLFMANU"]
    
    for audioFile in glob(audioFolderName + "*.*") :
        #Si le fichier est un fichier audio
        if (path.splitext(audioFile)[1] in AUDIO_TYPES) :
            transFile = transFolderName + path.splitext(path.basename(audioFile))[0] + ".*"
            transcripts = glob(transFile) #Liste des fichiers avec ce nom (sans extension)
            #Si au moins un fichier de transcription existe
            if (transcripts) :
                transFile = transcripts[0]
                transExt = path.splitext(transFile)[1]
                #Si le fichier de transcription est reconnu
                if (transExt in TRANSCRIPT_TYPES) :
                    mfccFileName = destFolderName + path.splitext(path.basename(audioFile))[0] + ".mfcc"
                    check_call([sys.executable, "convertToMfcc.py", audioFile, transFile, mfccFileName, configFile], shell=False)
                    if AFFICHAGE : print("Généré : " + mfccFileName)
                else :
                    if AFFICHAGE : print("Format transcript inconnu : " + transFile)
            else :
                if AFFICHAGE : print("Pas de transcript pour : " + audioFile)
        else :
            if AFFICHAGE : print("Format audio inconnu : " + audioFile)
                
if __name__ == '__main__':
    convertFolder(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
