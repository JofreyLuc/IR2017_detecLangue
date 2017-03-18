import sys,os
from subprocess import call
from platform import system             #Pour connaitre l'environnement d'execution
import csv

mfccFileName = sys.argv[1]

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
call(hListCall + " " + mfccFileName + " >> test.txt", shell = True)        

ifile = open("test.txt", 'r') 
ofile = open("sortie.txt", 'a', newline="")
wr = csv.writer(ofile, quoting=csv.QUOTE_ALL)
currentLine = ifile.readline()
while (currentLine != '') :
    if (not currentLine.startswith('-')) :
        currentLine += ifile.readline()
        mfcc = currentLine.split()[1:]
        mfcc = [float(x) for x in mfcc]
        wr.writerow(mfcc)
        
    currentLine = ifile.readline()
