import sys 
from platform import system            
from os import path, remove, makedirs 
import numpy as np
import h5py
from platform import system             
from subprocess import check_output, CalledProcessError, STDOUT     
from glob import glob
import configparser
import json


def parseConfig(configFilePath) :
    config = configparser.ConfigParser()
    config.read(configFilePath)
    
    HCOPY_PATH              = config.get('chemin_htk', 'chemin_executable_hcopy')
    HCOPY_CONFIG_FILE       = config.get('chemin_htk', 'chemin_config_hcopy')
    HLIST_PATH              = config.get('chemin_htk', 'chemin_executable_hlist')
    HLIST_CONFIG_FILE       = config.get('chemin_htk', 'chemin_config_hlist')

    TRAIN_AUDIO_FOLDER      = config.get('chemin_train', 'chemin_dossier_audio_train')
    TRAIN_TRANSCRIPTS_FOLDER = config.get('chemin_train', 'chemin_dossier_transcripts_train')
    TRAIN_MFCC_FOLDER       = config.get('chemin_train', 'chemin_dossier_mfcc_train')
    TRAIN_HDF5_FILE_PATH    = config.get('chemin_train', 'chemin_dossier_transcripts_train')
    
    DEV_AUDIO_FOLDER      = config.get('chemin_dev', 'chemin_dossier_audio_train')
    DEV_TRANSCRIPTS_FOLDER = config.get('chemin_dev', 'chemin_dossier_transcripts_train')
    DEV_MFCC_FOLDER       = config.get('chemin_dev', 'chemin_dossier_mfcc_train')
    DEV_HDF5_FILE_PATH    = config.get('chemin_dev', 'chemin_dossier_transcripts_train')
    
    TEST_AUDIO_FOLDER      = config.get('chemin_test', 'chemin_dossier_audio_train')
    TEST_TRANSCRIPTS_FOLDER = config.get('chemin_test', 'chemin_dossier_transcripts_train')
    TEST_MFCC_FOLDER       = config.get('chemin_test', 'chemin_dossier_mfcc_train')
    TEST_HDF5_FILE_PATH    = config.get('chemin_test', 'chemin_dossier_transcripts_train')
    
    AFFICHAGE = bool(config.get('param_pretraitement', 'affichage'))
    
    LANGUAGES = json.loads(config.get('liste_langages_formats', 'langues'))
    
    AUDIO_TYPES = json.loads(config.get('liste_langages_formats', 'formats_audio'))
    TRANSCRIPT_TYPES = json.loads(config.get('liste_langages_formats', 'formats_transcriptions'))
    
    
#Gestion de l'OS
linux=False
windows=False

# Met les variables d'OS à jour
def setOS() :
    if (system() == "Linux") :
        linux = True
    elif (system() == "Windows") :
        windows = True
    else :
        sys.exit("OS inconnu")


# Cherche le début et la fin de la coupe dans le fichier de transcription.
# Retourne les temps de début et de fin de la coupe en secondes.
# Format stm.
def searchBeginAndEndStm(transFileName):
    fileName = path.splitext(path.basename(transFileName))[0] # Nom du stm sans extension

    # On ouvre le fichier avec le bon encodage si celui-ci est précisé
    if (path.isfile(path.join(path.dirname(transFileName), "encoding.txt"))):
        e = open(path.join(path.dirname(transFileName) + "encoding.txt"), 'r')
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

# Coupe le fichier audio de cutBegin jusqu'à cutEnd (en secondes.)
def cutAudioFile(audioFileName, transFileName, outputFileName, beginningTime=None, endTime=None):
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

    # Calcule la durée du fichier coupé puis le coupe
    duration = cutEnd - cutBegin
    try:
        check_output("sox " + audioFileName + " " + cutFileName + " trim " + str(cutBegin) + " " + str(duration), shell = True, stderr=STDOUT)
    except CalledProcessError as exc:                                                                                          
        utils.eprintCalledProcessError(exc, "à SOX")
        sys.exit(1)
    
# Convertit un fichier en wav  
def convertAudioFileToWav(audioFileName, wavFileName):
    try :
        check_output("sox " + audioFileName + " " + wavFileName, shell = True, stderr=STDOUT)
    except CalledProcessError as exc :                                                                                          
        utils.eprintCalledProcessError(exc, "à SOX")
        sys.exit(1)

# Paramétrise un fichier 
def generateMfccFile(audioFileName, mfccFileName):
    if linux :
	    hCopyCall = "./" + HCOPY_PATH
    elif windows :
	    hCopyCall = HCOPY_PATH
    check_output(hCopyCall + " -C " + HCOPY_CONFIG_FILE + " " + audioFileName + " " + mfccFileName, shell = True, stderr=STDOUT)

# Crée un fichier avec la sortie de HList sur un fichier mfcc
def generateHListFromMfcc(mfccFileName, hListOutputFileName):
    if linux :
        hListCall = "./" + HLIST_PATH
    elif windows :
        hListCall = HLIST_PATH
    check_output(hListCall + " -C " + HLIST_CONFIG_FILE + " " + mfccFileName + " >> " + hListOutputFileName, shell = True, stderr=STDOUT)  

# Coupe un fichier puis crée le mfcc correspondant        
def cutFileThenGenerateMfcc(audioFileName, mfccFileName, transFileName=None) :
        
    audioName = path.splitext(path.basename(audioFileName))[0] #Nom du fichier audio sans extension
    
    #Conversion en wav (dans tous les cas)
    wavFileName = audioName + "_temp.wav"
    convertAudioFileToWav(audioFileName, wavFileName)
    audioFileName = wavFileName

    #Coupe de l'audio
    if (transFileName is not None) :
        cutFileName = path.splitext(audioName)[0] + "_trimmed.wav"
        cutAudioFile(audioFileName, transFileName, cutFileName)

    #Génération des mfcc
    try :
        generateMfccFile(cutFileName, mfccFileName)
    except CalledProcessError as exc :
        utils.eprintCalledProcessError(exc, "à HCopy (HTK)")

    #Suppression des fichiers de transition
    remove(wavFileName)
    remove(cutFileName)
    
# Renvoie un bon fichier de transcript (si il existe)    
def getValidTransFile(audioFileName, transFolderName):  
    transFile = transFolderName + path.splitext(path.basename(audioFile))[0] + ".*"
    transcripts = glob(transFile) #Liste des fichiers avec ce nom (sans extension)
    #Si au moins un fichier de transcription existe
    for file in transcripts :
        ext = path.splitext(file)[1]
        #Si le fichier de transcription est reconnu
        if (ext in TRANSCRIPT_TYPES) :
            return file
    return None

#Script pour transformer un dossier de fichiers audio (et leur transcription) en fichiers .mfcc
def generateMfccFolder(audioFolderName, destFolderName, transFolderName=None) :

    #Pour tous les fichiers dans le répertoire audio
    for audioFile in glob(audioFolderName + "*.*") :
        #Si le fichier est un fichier audio
        if (path.splitext(audioFile)[1] not in AUDIO_TYPES) :
            eprint("Format audio inconnu : " + audioFile)
            continue
        
        #Si on a des transcriptions
        if (transFolderName is not None) :
            transFileName = getValidTransFile(audioFile, transFolderName)
            if (transFileName is None) :
                eprint("Pas de fichier de transcription valide pour : " + audioFile)
                
        #Génération mfcc
        mfccFileName = destFolderName + path.splitext(path.basename(audioFile))[0] + ".mfcc"
        cutFileThenGenerateMfcc(audioFileName, mfccFileName, transFileName)
        if AFFICHAGE : print("Généré : " + mfccFileName)
        
#Script pour transformer tous les dossiers du corpus en fichiers mfcc
def generateAllMfcc() :

    CORPUSES = [(TRAIN_AUDIO_FOLDER, TRAIN_TRANS_FOLDER, TRAIN_MFCC_FOLDER),
                (DEV_AUDIO_FOLDER, DEV_TRANS_FOLDER, DEV_MFCC_FOLDER),
                (TEST_AUDIO_FOLDER, TEST_TRANS_FOLDER, TEST_MFCC_FOLDER)]
    
    for (audioFolder, transFolder, mfccFolder) in CORPUSES:
        if (audioFolder is not None and mfccFolder is not None):
            if not path.exists(mfccFolder) : makedirs(mfccFolder)
            for lang in LANGUAGES :
                if not path.exists(path.join(mfccFolder, lang)) : makedirs(path.join(mfccFolder, lang))
                generateMfccFolder(audioFolder, mfccFolder, transFolder)

# Ajoute un fichier mfcc dans un fichier hdf5
def convertMfccToHdf5(mfccFileName, language, hdf5File) :
        
    TEMP_FILE = "HListTmp" #Fichier texte temporaire généré par HList
        
    generateHListFromMfcc(mfccFileName, TEMP_FILE)

    ifile = open(TEMP_FILE, 'r') #Fichier d'entrée
    currentLine = ifile.readline()
    
    mfcc = []
    #Pour tout le fichier
    while (currentLine != '') :
        #Si on est sur une ligne de donnése
        if (not currentLine.startswith('-')) :
            #On lit la ligne suivante, on ajoute la langue et on écrit dans le buffer
            currentLine += ifile.readline()
            mfccRow = currentLine.split()[1:]
            mfccRow.append(language)
            mfccRow = [float(i) for i in mfccRow]
            mfcc.append(mfccRow)
   
        currentLine = ifile.readline()
    
    ifile.close()
    remove(TEMP_FILE)
    
    npMfcc = np.asarray(mfcc)
    #création du conteneur HDF5
    hdf5Out = h5py.File(hdf5File, "a")
    #on crée 1 dataset hdf5 pour ce fichier mfcc 
    fileName = path.splitext(path.basename(mfccFileName))[0] #Nom du fichier sans extension
    hdf5Out.create_dataset(fileName, data=npMfcc)
    hdf5Out.close()

#Ajoute tous les fichiers mfcc d'un dossier dans un fichier hdf5
def convertMfccFolderToHdf5(mfccFolderName, language, hdf5File):
    standardFileName = path.join(mfccFolderName + "*.mfcc")
    for file in glob(standardFileName) :
        convertMfccToHdf5.py(file, language, hdf5File)
        if AFFICHAGE : print("Traité : " + file)

#Ajoute tous les fichiers mfcc du corpus dans un fichier hdf5
def convertAllMfccToHdf5() :

    CORPUSES = [(TRAIN_MFCC_FOLDER, TRAIN_HDF5_FILE_PATH), (DEV_MFCC_FOLDER, DEV_HDF5_FILE_PATH), (TEST_MFCC_FOLDER, TEST_HDF5_FILE_PATH)]
    
    for (mfccFolder, hdf5FilePath) in CORPUSES:
        if (mfccFolder is not None and hdf5FilePath is not None):
            if path.isfile(hdf5FilePath) : remove(hdf5FilePath) 
            for lang in LANGUAGES :
                convertMfccToHdf5(mfccFolder, str(LANGUAGES.index(lang)), hdf5FilePath)
