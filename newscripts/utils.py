# Module python contenant quelques fonctions utiles.

import sys
from os import path
from subprocess import CalledProcessError

# Ecrit sur stderr.
def eprint(*args, **kwargs) :
    print(*args, file=sys.stderr, **kwargs)
    
def eprintCalledProcessError(exc, processName) :
    if isinstance(exc, CalledProcessError) :    # Si il s'agit bien de ce type d'erreur 
        eprint("Erreur lors de l'appel ", processName, " (returncode : ", exc.returncode, ") :\n", exc.output.decode(sys.stdout.encoding))
