#!/usr/bin/env python3
#Script pour transformer un fichier audio de dev/test en .mfcc
#python3 convertFileToMfcc.py audio.* resultat.mfcc confightk

from os import path                     #Pour couper l'extension de fichier
from os import remove                   #Pour supprimer des fichiers
import sys                              #Pour récuperer les arguments du programme
from subprocess import check_output, CalledProcessError, STDOUT, call     #Pour lancer sox, htk et les scripts python
from platform import system             #Pour connaitre l'environnement d'exécution

def convertFileToMfcc(audioFileName, mfccFileName, configFile) :
    
    #Gestion de l'OS
    linux=False
    windows=False
    if (system() == "Linux") :
        linux = True
    elif (system() == "Windows") :
        windows = True
    else :
        sys.exit("OS inconnu")

    hasBeenConverted = False    #Indique si on a du convertir le fichier en .wav
        
    audioName = path.splitext(path.basename(audioFileName))[0] #Nom du fichier audio sans extension
    
    wavFileName = audioName + ".wav"
    try :
        check_output("sox " + audioFileName + " " + wavFileName, shell = True, stderr=STDOUT)
    except CalledProcessError as exc :                                                                                          
        print("Erreur lors de l'appel à SOX (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
        sys.exit(1)
    audioName = wavFileName
    hasBeenConverted = True


        #Génération des mfcc
    if (linux) :
	    hCopyCall = "./HCopy"
    elif (windows) :
	    hCopyCall = "HCopy"
    try :
        check_output(hCopyCall + " -C " + configFile + " " + audioName + " " + mfccFileName, shell = True, stderr=STDOUT)
    except CalledProcessError as exc :
        print("Fichier responsable : ", audioFileName)
        print("Erreur lors de l'appel à HCopy (HTK) (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
        sys.exit(1)

    #Suppression des fichiers de transition
    if (hasBeenConverted) :
        remove(wavFileName)


if __name__ == '__main__':
    convertFileToMfcc(sys.argv[1], sys.argv[2], sys.argv[3])
