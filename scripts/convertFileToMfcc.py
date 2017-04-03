#!/usr/bin/env python3
#Script pour transformer un fichier audio en .mfcc
#python3 convertFileToMfcc.py audio.* transcript.stm resultat.mfcc confightk

from os import path                     #Pour couper l'extension de fichier
from os import remove                   #Pour supprimer des fichiers
import sys                              #Pour récuperer les arguments du programme
from subprocess import check_output, CalledProcessError, STDOUT, call     #Pour lancer sox, htk et les scripts python
from platform import system             #Pour connaitre l'environnement d'exécution

def convertFileToMfcc(audioFileName, transFileName, mfccFileName, configFile) :
    
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
    
    #Conversion en wav si besoin
    if (path.splitext(audioFileName)[1] != ".wav") :
        wavFileName = audioName + ".wav"
        try :
            check_output("sox " + audioFileName + " " + wavFileName, shell = True, stderr=STDOUT)
        except CalledProcessError as exc :                                                                                          
            print("Erreur lors de l'appel à SOX (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
            sys.exit(1)
        audioName = wavFileName
        hasBeenConverted = True

    #Coupe de l'audio
    cutFileName = path.splitext(audioName)[0] + "_trimmed.wav"
    try :
        check_output([sys.executable, "cutAudioFile.py", audioFileName, transFileName, cutFileName], shell=False, stderr=STDOUT)
    except CalledProcessError as exc :                                                                                          
        print("Erreur lors de l'appel du script cutAudioFile.py (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
        sys.exit(1)

        #Génération des mfcc
    if (linux) :
	    hCopyCall = "./HCopy"
    elif (windows) :
	    hCopyCall = "HCopy"
    try :
        check_output(hCopyCall + " -C " + configFile + " " + cutFileName + " " + mfccFileName, shell = True, stderr=STDOUT)
    except CalledProcessError as exc :                                                                                          
        print("Erreur lors de l'appel à HCopy (HTK) (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
        sys.exit(1)

    #Suppression des fichiers de transition
    if (hasBeenConverted) :
        remove(wavFileName)
    remove(cutFileName)


if __name__ == '__main__':
    convertFileToMfcc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
