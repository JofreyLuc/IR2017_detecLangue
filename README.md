Nécessite python3.

Se placer dans le dossier `scripts/` pour exécuter les scripts. 

# Pré-traitement

`python3 preTraitement.py`

Arborescence nécessaire :
* `scripts/` contient les scripts python + executables HTK
* `corpus/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers audio du corpus
* `transcripts/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers de transcription du corpus
* `mfcc/` contiendra les résultats de la conversion

**IMPORTANT** : copier le fichier `scripts/encoding.txt` dans `transcripts/french/` avant de lancer le traitement