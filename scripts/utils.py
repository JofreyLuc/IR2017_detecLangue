# Module python contenant quelques fonctions utiles.

import sys
from os import path
from argparse import ArgumentTypeError
from subprocess import CalledProcessError

# Ecrit sur stderr.
def eprint(*args, **kwargs) :
    print(*args, file=sys.stderr, **kwargs)
    
def eprintCalledProcessError(exc, processName) :
    if isinstance(exc, CalledProcessError) :    # Si il s'agit bien de ce type d'erreur 
        eprint("Erreur lors de l'appel ", processName, " (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
    
###############################################################
## Fonctions pouvant levées des exceptions ArgumentTypeError ##
## à utiliser dans le parsing d'arguments.                   ##
###############################################################

# Vérifie si la chaîne de caractères passées en paramètres correspond bien à un fichier existant.
def isValidFile(fileName) :
    if not path.isfile(fileName) :
        raise ArgumentTypeError("%s n'existe pas ou n'est pas un fichier valide." % fileName)
    return fileName  # retourne le nom du fichier

# Vérifie si la chaîne de caractères passées en paramètres correspond bien à un fichier de transcription existant et dont le format est supporté.
def isValidTranscriptFile(fileName) :
    isValidFile(fileName)
    extension = path.splitext(fileName)[1]
    #print(extension)
    if extension != ".stm" and extension != ".mlfmanu" :
        raise ArgumentTypeError("L'extension %s n'est pas une extension de transcription valide ou n'est pas supportée." % extension)
    return fileName  # retourne le nom du fichier
    
# Vérifie si le paramètre est bien un nombre positif.
def isPositiveNumber(string) :
    try :
        value = float(string)
        if value < 0 :
            raise ArgumentTypeError("%s n'est pas un nombre positif." % string)
    except ValueError :
        raise ArgumentTypeError("%s n'est pas un nombre positif." % string)
    return value