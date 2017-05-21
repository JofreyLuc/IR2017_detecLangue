#!/usr/bin/env python3
#Script pour transformer un dossier de fichiers audio de dev/test en fichiers .mfcc
#python3 convertFolderToMfcc.py audio/ dest/ confightk

from subprocess import check_call #Pour appeller le script de conversion
from os import path               #Pour récupérer les noms de fichier/extensions
import sys                        #Pour les arguments du programme
from glob import glob             #Pour lister des fichiers

def convertFolderToMfcc(audioFolderName, destFolderName, configFile) :

    AFFICHAGE = True #Active ou désactive l'affichage au cours de la conversion
    AUDIO_TYPES = [".wav", ".WAV", ".sph", ".SPH"] #Formats d'audio reconnus

    #Pour tous les fichiers dans le répertoire audio
    for audioFile in glob(audioFolderName + "*.*") :
        #Si le fichier est un fichier audio
        if (path.splitext(audioFile)[1] in AUDIO_TYPES) :
            mfccFileName = destFolderName + path.splitext(path.basename(audioFile))[0] + ".mfcc"
            check_call([sys.executable, "convertFileToMfccWITHOUTTRANS.py", audioFile, mfccFileName, configFile], shell=False)
            if AFFICHAGE : print("Généré : " + mfccFileName)
        else :
            if AFFICHAGE : print("Format audio inconnu : " + audioFile)
                
if __name__ == '__main__':
    convertFolderToMfcc(sys.argv[1], sys.argv[2], sys.argv[3])
