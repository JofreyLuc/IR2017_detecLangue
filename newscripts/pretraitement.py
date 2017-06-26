import sys 
from platform import system            
from os import path, remove, makedirs 
import numpy as np
import h5py
from platform import system             
from subprocess import check_output, CalledProcessError, STDOUT     
from glob import glob
from utils import eprint, eprintCalledProcessError
import configparser
import json

#Gestion de l'OS
linux=False
windows=False

def parseConfig(configFilePath) :
    config = configparser.ConfigParser()
    config.read(configFilePath)

    global HCOPY_PATH, HCOPY_CONFIG_FILE, HLIST_PATH, HLIST_CONFIG_FILE
    global TRAIN_AUDIO_FOLDER, TRAIN_TRANSCRIPTS_FOLDER, TRAIN_MFCC_FOLDER, TRAIN_HDF5_FILE_PATH
    global DEV_AUDIO_FOLDER, DEV_TRANSCRIPTS_FOLDER, DEV_MFCC_FOLDER, DEV_HDF5_FILE_PATH
    global TEST_AUDIO_FOLDER, TEST_TRANSCRIPTS_FOLDER, TEST_MFCC_FOLDER, TEST_HDF5_FILE_PATH
    global AFFICHAGE, LANGUAGES, AUDIO_TYPES, TRANSCRIPT_TYPES
    global SHIFT, NB_TRAMES, NB_EPOCHS
    
    HCOPY_PATH              = config.get('chemin_htk', 'chemin_executable_hcopy')
    HCOPY_CONFIG_FILE       = config.get('chemin_htk', 'chemin_config_hcopy')
    HLIST_PATH              = config.get('chemin_htk', 'chemin_executable_hlist')
    HLIST_CONFIG_FILE       = config.get('chemin_htk', 'chemin_config_hlist')

    TRAIN_AUDIO_FOLDER      = config.get('chemin_train', 'chemin_dossier_audio_train')
    TRAIN_TRANSCRIPTS_FOLDER = config.get('chemin_train', 'chemin_dossier_transcripts_train')
    TRAIN_MFCC_FOLDER       = config.get('chemin_train', 'chemin_dossier_mfcc_train')
    TRAIN_HDF5_FILE_PATH    = config.get('chemin_train', 'chemin_hdf5_train')
    
    DEV_AUDIO_FOLDER      = config.get('chemin_dev', 'chemin_dossier_audio_dev')
    DEV_TRANSCRIPTS_FOLDER = config.get('chemin_dev', 'chemin_dossier_transcripts_dev')
    DEV_MFCC_FOLDER       = config.get('chemin_dev', 'chemin_dossier_mfcc_dev')
    DEV_HDF5_FILE_PATH    = config.get('chemin_dev', 'chemin_hdf5_dev')
    
    TEST_AUDIO_FOLDER      = config.get('chemin_test', 'chemin_dossier_audio_test')
    TEST_TRANSCRIPTS_FOLDER = config.get('chemin_test', 'chemin_dossier_transcripts_test')
    TEST_MFCC_FOLDER       = config.get('chemin_test', 'chemin_dossier_mfcc_test')
    TEST_HDF5_FILE_PATH    = config.get('chemin_test', 'chemin_hdf5_test')
    
    LANGUAGES = json.loads(config.get('liste_langages_formats', 'langues'))
    
    AUDIO_TYPES = json.loads(config.get('liste_langages_formats', 'formats_audio'))
    TRANSCRIPT_TYPES = json.loads(config.get('liste_langages_formats', 'formats_transcriptions'))

    AFFICHAGE = bool(config.get('param_pretraitement', 'affichage'))

    SHIFT = config.get('param_reseau', 'decalage')
    NB_TRAMES = config.get('param_reseau', 'nombre_trames')
    NB_EPOCHS = config.get('param_reseau', 'nombre_epoch')

# Met les variables d'OS à jour
def setOS() :
    global linux
    global windows
    if (system() == "Linux") :
        linux = True
    elif (system() == "Windows") :
        windows = True
    else :
        sys.exit("OS inconnu")


# Cherche le début et la fin de la coupe dans le fichier de transcription.
# Retourne les temps de début et de fin de la coupe en secondes.
# Format stm.
def searchBeginAndEndStm(transFilePath):
    transFileName = path.splitext(path.basename(transFilePath))[0] # Nom du stm sans extension
    
    # On ouvre le fichier avec le bon encodage si celui-ci est précisé
    if (path.isfile(path.join(path.dirname(transFilePath), "encoding.txt"))):
        e = open(path.join(path.dirname(transFilePath), "encoding.txt"), 'r')
        encod = e.readline()
        f = open(transFilePath, 'r', encoding=encod)
        e.close()
    else:
        f = open(transFilePath, 'r')

    #Tant qu'on a pas une ligne de transcription (commencant par le nom de fichier) on lit en avancant
    currentLine = f.readline()
    while (currentLine.split()[0] != transFileName):
        currentLine = f.readline()

    #Si la première ligne est un silence/musique, on prend comme début le timestamp de fin, sinon le timestamp de début
    if (currentLine.split()[2] == "inter_segment_gap"):
        beginning = float(currentLine.split()[4])
    else:
        beginning = float(currentLine.split()[3])
            
    #On va jusqu'à la fin du fichier en conservant la dernière ligne "correcte"
    nextLine = f.readline()
    while (nextLine != ''):
        if (nextLine.split()[0] == transFileName and nextLine.split()[2] != "inter_segment_gap"):
            currentLine = nextLine
        nextLine = f.readline()

    #On prend la fin de la dernière phrase
    end = float(currentLine.split()[4])     
    
    f.close()

    return (beginning, end)

# Cherche le début et la fin de la coupe dans le fichier de transcription.
# Retourne les temps de début et de fin de la coupe en secondes.
# Format mlfmanu.
def searchBeginAndEndMlfmanu(transFilePath):    
    f = open(transFilePath, 'r')
    currentLine = f.readline()
    # On lit le fichier ligne par ligne tant qu'on a pas atteint une ligne non vide,
    # qui n'est pas un commentaire ou qui n'est pas un silence.
    while (currentLine[0] == "#" or currentLine[0] == "\"" or currentLine.split()[2] == "sil"):
        currentLine = f.readline()

    beginning = float(currentLine.split()[0]) / 10000000; #Conversion en secondes

    nextLine = f.readline()
    # On lit ligne par ligne tant qu'on a pas atteint la dernière ligne (ligne de silence exclus)
    while (nextLine[0] != '.'):
        if (nextLine.split()[2] != "sil"):
            currentLine = nextLine
        nextLine = f.readline()
            
    end = float(currentLine.split()[1]) / 10000000; #Conversion en secondes
    
    f.close()
    
    return (beginning, end)

# Coupe le fichier audio de cutBegin jusqu'à cutEnd (en secondes.)
def cutAudioFile(audioFilePath, transFilePath, outputFilePath, beginningTimeMin=None, endTimeMin=None):
    extension = path.splitext(transFilePath)[1]
    if (extension == ".stm"):
        (beginning, ending) = searchBeginAndEndStm(transFilePath)
    elif (extension == ".mlfmanu"):
        (beginning, ending) = searchBeginAndEndMlfmanu(transFilePath)
        
    # On prend les temps "les plus limitants"
    if (beginningTimeMin is not None and beginningTimeMin > beginning):
        beginning = beginningTimeMin
    if (endTimeMin is not None and endTimeMin < ending):
        ending = endTimeMin

    # Calcule la durée du fichier coupé puis le coupe
    duration = ending - beginning
    try:
        check_output("sox " + audioFilePath + " " + outputFilePath + " trim " + str(beginning) + " " + str(duration), shell = True, stderr=STDOUT)
    except CalledProcessError as exc:                                                                                          
        eprintCalledProcessError(exc, "à SOX")
        sys.exit(1)
    
# Convertit un fichier en wav  
def convertAudioFileToWav(audioFilePath, wavFilePath):
    try :
        check_output("sox " + audioFilePath + " " + wavFilePath, shell = True, stderr=STDOUT)
    except CalledProcessError as exc :                                                                                          
        eprintCalledProcessError(exc, "à SOX")
        sys.exit(1)

# Paramétrise un fichier 
def generateMfccFile(audioFilePath, mfccFilePath):
    if linux :
	    hCopyCall = "./" + HCOPY_PATH
    elif windows :
	    hCopyCall = HCOPY_PATH
    check_output(hCopyCall + " -C " + HCOPY_CONFIG_FILE + " " + audioFilePath + " " + mfccFilePath, shell = True, stderr=STDOUT)

# Crée un fichier avec la sortie de HList sur un fichier mfcc
def generateHListFromMfcc(mfccFilePath, hListOutputFilePath):
    if linux :
        hListCall = "./" + HLIST_PATH
    elif windows :
        hListCall = HLIST_PATH
    check_output(hListCall + " -C " + HLIST_CONFIG_FILE + " " + mfccFilePath + " >> " + hListOutputFilePath, shell = True, stderr=STDOUT)  

# Coupe un fichier puis crée le mfcc correspondant        
def cutFileThenGenerateMfcc(audioFilePath, mfccFilePath, transFilePath=None) :

    removeJustOne = False
    
    audioPathWithoutExt = path.splitext(audioFilePath)[0] #Chemin du fichier audio sans extension
    
    #Conversion en wav (dans tous les cas)
    wavFilePath = audioPathWithoutExt + "_temp.wav"
    convertAudioFileToWav(audioFilePath, wavFilePath)

    #Coupe de l'audio
    if (transFilePath is not None) :
        cutFilePath = audioPathWithoutExt + "_trimmed.wav"
        cutAudioFile(wavFilePath, transFilePath, cutFilePath)
    else :
        cutFilePath = wavFilePath
        removeJustOne = True
        
    #Génération des mfcc
    try :
        generateMfccFile(cutFilePath, mfccFilePath)
    except CalledProcessError as exc :
        eprintCalledProcessError(exc, "à HCopy (HTK)")

    #Suppression des fichiers de transition
    if (not removeJustOne) : remove(wavFilePath)
    remove(cutFilePath)
    
# Renvoie un bon fichier de transcript (si il existe)    
def getValidTransFile(audioFilePath, transFolderPath):
    transFilePath = path.join(transFolderPath, path.splitext(path.basename(audioFilePath))[0] + ".*")
    transcripts = glob(transFilePath) #Liste des fichiers avec ce nom (sans extension)
    #Si au moins un fichier de transcription existe
    for transFile in transcripts :
        ext = path.splitext(transFile)[1]
        #Si le fichier de transcription est reconnu
        if (ext in TRANSCRIPT_TYPES) :
            return transFile
    return None

#Script pour transformer un dossier de fichiers audio (et leur transcription) en fichiers .mfcc
def generateMfccFolder(audioFolderPath, destFolderPath, transFolderPath=None) :
    
    #Pour tous les fichiers dans le répertoire audio
    for audioFile in glob(path.join(audioFolderPath, "*.*")) :
        #Si le fichier est un fichier audio
        if (path.splitext(audioFile)[1] not in AUDIO_TYPES) :
            eprint("Format audio inconnu : " + audioFile)
            continue
        
        #Si on a des transcriptions
        if (transFolderPath is not None) :
            transFilePath = getValidTransFile(audioFile, transFolderPath)
            if (transFilePath is None) :
                eprint("Pas de fichier de transcription valide dans " + transFolderPath + " pour : " + audioFile)
        
        #Génération mfcc
        mfccFilePath = path.join(destFolderPath, path.splitext(path.basename(audioFile))[0] + ".mfcc")
        cutFileThenGenerateMfcc(audioFile, mfccFilePath, transFilePath)
        if AFFICHAGE : print("Généré : " + mfccFilePath)
        
#Script pour transformer tous les dossiers du corpus en fichiers mfcc
def generateAllMfcc() :

    CORPUSES = [(TRAIN_AUDIO_FOLDER, TRAIN_TRANSCRIPTS_FOLDER, TRAIN_MFCC_FOLDER),
                (DEV_AUDIO_FOLDER, DEV_TRANSCRIPTS_FOLDER, DEV_MFCC_FOLDER),
                (TEST_AUDIO_FOLDER, TEST_TRANSCRIPTS_FOLDER, TEST_MFCC_FOLDER)]
    
    for (audioFolder, transFolder, mfccFolder) in CORPUSES:
        if audioFolder and mfccFolder : # not None and not empty
            if not path.exists(mfccFolder) : makedirs(mfccFolder)
            for lang in LANGUAGES :
                if not path.exists(path.join(mfccFolder, lang)) : makedirs(path.join(mfccFolder, lang))
                generateMfccFolder(path.join(audioFolder, lang), path.join(mfccFolder, lang), path.join(transFolder, lang))

# Ajoute un fichier mfcc dans un fichier hdf5
def convertMfccToHdf5(mfccFilePath, language, hdf5FilePath) :
        
    TEMP_FILE = path.join(path.dirname(mfccFilePath), "HListTmp") #Fichier texte temporaire généré par HList
        
    generateHListFromMfcc(mfccFilePath, TEMP_FILE)
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
    hdf5Out = h5py.File(hdf5FilePath, "a")
    #on crée 1 dataset hdf5 pour ce fichier mfcc 
    fileName = path.splitext(path.basename(mfccFilePath))[0] #Nom du fichier sans extension
    hdf5Out.create_dataset(fileName, data=npMfcc)
    hdf5Out.close()

#Ajoute tous les fichiers mfcc d'un dossier dans un fichier hdf5
def convertMfccFolderToHdf5(mfccFolderPath, language, hdf5FilePath):
    standardFilePath = path.join(mfccFolderPath, "*.mfcc")
    for mfccFile in glob(standardFilePath) :
        convertMfccToHdf5(mfccFile, language, hdf5FilePath)
        if AFFICHAGE : print("Traité : " + mfccFile)

#Ajoute tous les fichiers mfcc du corpus dans un fichier hdf5
def convertAllMfccToHdf5() :

    CORPUSES = [(TRAIN_MFCC_FOLDER, TRAIN_HDF5_FILE_PATH), (DEV_MFCC_FOLDER, DEV_HDF5_FILE_PATH), (TEST_MFCC_FOLDER, TEST_HDF5_FILE_PATH)]
    
    for (mfccFolder, hdf5FilePath) in CORPUSES:
        if mfccFolder and hdf5FilePath: # Not None et not empty
            if path.isfile(hdf5FilePath) : remove(hdf5FilePath) 
            for lang in LANGUAGES :
                convertMfccFolderToHdf5(path.join(mfccFolder, lang), str(LANGUAGES.index(lang)), hdf5FilePath)
