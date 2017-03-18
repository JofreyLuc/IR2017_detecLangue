Nécessite python3.

#Conversion

`python3 convertAll.py`

Arborescence par défaut (dans `convertAll.py`) :
* `scripts/` contient les scripts python + executables HTK
* `corpus/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers audio du corpus
* `transcripts/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers de transcription du corpus
* `mfcc/` contiendra les résultats de la conversion

**IMPORTANT** : copier le fichier `scripts/encoding.txt` dans `corpus/french/` avant de lancer la conversion