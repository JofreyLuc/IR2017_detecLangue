#Script pour couper le début et la fin de non-parole des fichiers anglais
#python3 cuttingEnglish.py transcript.stm audio.sph

from os import path #Pour couper l'extension de fichier
import sys #Pour récuperer les arguments du programme
from subprocess import call #Pour lancer le bash sox

filenameExt = sys.argv[1]
audiofileName = sys.argv[2]
cutFileName = sys.argv[3]
filename = path.splitext(filenameExt)[0] #Nom du stm sans extension

#On calcule la taille du début de chaque ligne (= tout ce qui est avant le timestamp) 
lineHeaderSize = len(filename) * 2 + 4

f = open(filenameExt, 'r')
currentLine = f.readline()
currentLine = currentLine[lineHeaderSize:] #On coupe le début de la ligne

#On va récupérer les valeurs flottantes dans la ligne
temps = []
for e in currentLine.split():
    try:
        temps.append(float(e))
    except ValueError:
        pass

#On prend la première de ces valeurs
debut = temps[0]

#On va jusqu'à l'avant-dernière ligne du fichier (la dernière est vide)
nextLine = f.readline()
while (nextLine) :
    currentLine = nextLine
    nextLine = f.readline()
    
currentLine = currentLine[lineHeaderSize:]

temps = []
for e in currentLine.split():
    try:
        temps.append(float(e))
    except ValueError:
        pass

#On prend la deuxième valeur du dernier timestamp
fin = temps[1]

duree = fin - debut

f.close()

#On appelle le script bash qui va couper le fichier avec sox
call("sox " + audiofileName + " " + cutFileName + " trim " + str(debut) + " " + str(duree), shell = True)
