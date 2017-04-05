Nécessite python3.

Se placer dans le dossier `scripts/` pour exécuter les scripts. 

Arborescence nécessaire :

* `scripts/` contient les scripts python + executables HTK

* `train/corpus/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers audio du corpus de train
* `train/transcripts/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers de transcription du corpus de train
* `dev/corpus/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers audio du corpus de dev
* `dev/transcripts/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers de transcription du corpus de dev
* `test/corpus/` contient `arabic/`, `english/`, `french/`, `german/` qui contiennent les fichiers audio du corpus de test

* `mfcc/` contiendra les résultats de la conversion des fichiers du train
* `mfccdev/` contiendra les résultats de la conversion des fichiers du dev
* `mfcctest/` contiendra les résultats de la conversion des fichiers du test

**IMPORTANT** : copier le fichier `scripts/encoding.txt` dans `train/transcripts/french/` avant de lancer le traitement