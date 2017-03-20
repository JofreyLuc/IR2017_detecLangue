import sys,os
from subprocess import call
from platform import system             #Pour connaitre l'environnement d'execution
import csv
from os import remove                   #Pour supprimer des fichiers

tmpFile = "HListTmp"

mfccFileName = sys.argv[1]
language = sys.argv[2]
outputFile = sys.argv[3]

#Gestion de l'OS
linux=False
windows=False
if (system() == "Linux") :
    linux = True
elif (system() == "Windows") :
    windows = True
else :
    sys.exit("OS inconnu")
    
#Génération des mfcc
if (linux) :
    hListCall = "./HList"
elif (windows) :
    hListCall = "HList"
call(hListCall + " " + mfccFileName + " >> " + tmpFile, shell = True)        

ifile = open(tmpFile, 'r') 
ofile = open(outputFile, 'a', newline="")
wr = csv.writer(ofile)
currentLine = ifile.readline()
while (currentLine != '') :
    if (not currentLine.startswith('-')) :
        currentLine += ifile.readline()
        mfcc = currentLine.split()[1:]
        mfcc.append(language)
        wr.writerow(mfcc)
   
    currentLine = ifile.readline()

ifile.close()
ofile.close()    
remove(tmpFile)
