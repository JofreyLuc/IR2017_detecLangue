#!/usr/bin/env python3
#Script pour transformer un dossier de fichiers audio (et leur transcription) en fichiers .mfcc
#python3 convertFolder.py audio/ transcript/ dest/ confightk

import convertToMfcc
from os import path, listdir
import sys

def convertFolder(audioFolderName, transFolderName, destFolderName, configFile) :

    for file in listdir(audioFolderName) :
        if (file.endswith(".sph") or file.endswith(".wav")) :
            transFile = transFolderName + "/" + path.splitext(path.basename(file))[0]
            if (path.isFile(transFile)) :
                print(transName)

if __name__ == '__main__':
    convertFolder(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
            
