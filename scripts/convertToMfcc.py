#Script pour transformer un fichier audio en .mfcc
#python3 audio.sph transcript.stm confightk

import cuttingEnglish
import os
import sys
from subprocess import call
from subprocess import Popen

audioFileName = sys.argv[1]
transFileName = sys.argv[2]

#Conversion en wav si besoin
if (os.path.splitext(audioFileName)[1] != ".wav") :
    wavFileName = os.path.splitext(audioFileName)[0] + ".wav"
    call("sox " + audioFileName + " " + wavFileName, shell = True)
    audioFileName = wavFileName

#Coupe de l'audio
cutFileName = os.path.splitext(audioFileName)[0] + "_trimmed.wav"
call("python3 cuttingEnglish.py " + transFileName + " " + audioFileName + " " + cutFileName, shell = True)


#Génération des mfcc
configFile = sys.argv[3]
mfcFileName = os.path.splitext(audioFileName)[0] + ".mfcc"
call("./HCopy -C " + configFile + " " + cutFileName + " " + mfcFileName, shell = True) 
