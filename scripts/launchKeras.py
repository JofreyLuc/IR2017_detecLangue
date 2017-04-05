# Crée un réseau de neurones avec Keras

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
import numpy as np
import h5py
import sys
from os import remove

# Paramètres
# Nombre de coefficients cepstraux
nbCoef = 13
# Nombre de valeurs à prélever pour obtenir une "fenêtre de parole"
nbVal = 31
# Décalage entre chaque prélevement de fenêtre de parole
shift = 10

# On récupère les données
dataFile = sys.argv[1]
hdf5In = h5py.File(dataFile, "r")

# Calcul du nombre total de fenêtres de parole de la base d'apprentissage
# Une fenêtre est une matrice contenant des coefficients cepstraux :
# - de nbVal lignes 
# - de nbCoef colonnes
totalFrames = 0
for dataset in hdf5In.values():                             # Pour chaque dataset du fichier hdf5
    frames = int ((dataset.shape[0] - nbVal) / shift) + 1   # Nb fenêtres du dataset
    totalFrames += frames
    
# Création d'un fichier hdf5 temporaire afin de stocker notre base d'apprentissage
# formaté correctement pour keras afin de ne pas charger les données en mémoire vive
tmpFile = "tmp.hdf5"
hdf5Tmp = h5py.File(tmpFile, "w")
hdf5Tmp.create_dataset("examples", (totalFrames, nbVal * nbCoef)) # dataset données
hdf5Tmp.create_dataset("languages", (totalFrames,))               # dataset étiquettes
X = hdf5Tmp.get("examples")
Y = hdf5Tmp.get("languages")

frameIndex = 0
# Parcours des datasets du fichier d'entrée afin de remplir les datasets temporaires
for dataset in hdf5In.values():
    print(dataset)
    # On prend chaque fenêtre de parole du dataset courant
    for frameStartIndex in range(0, len(dataset) - nbVal, shift):
        # Une fenêtre de nbVal vecteurs
        frameVectors = dataset[frameStartIndex : frameStartIndex + nbVal]
        # On prend le langage sur le premier vecteur de la fenêtre (dernière valeur du vecteur)
        language = frameVectors[0][len(frameVectors[0])-1]
        vectorIndex = 0
        # On va stocker les valeurs de la fenêtre de parole dans un tableau numpy temporaire
        # cela permet d'accélerer le remplissage des datasets temporaires
        frameValues = np.empty([nbVal * nbCoef])
        # Pour chaque vecteur (contenant nbCoef valeurs) de la fenêtre courante
        for vector in frameVectors :
            # On remplit le tableau de la fenêtre de parole avec les coefficients du vecteur
            frameValues[vectorIndex : vectorIndex + nbCoef] = vector[0 : nbCoef]
            vectorIndex += 13  # au fur et à mesure

        # On remplit le dataset data avec les coefficients du vecteur
        X[frameIndex] = frameValues
        Y[frameIndex] = language
        frameIndex += 1

hdf5In.close()
        
# On met les étiquettes sous forme de vecteurs binaires pour keras
Y = to_categorical(Y)

# On crée le modèle séquentiel, avec 4 couches
inputShape = nbVal * nbCoef
model = Sequential()
model.add(Dropout(0.2, input_shape=(inputShape,)))
model.add(Dense(inputShape, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(4, kernel_initializer='normal', activation='softmax'))

# On compile le modèle
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

# On entraîne le modèle
model.fit(X, Y, epochs=10, batch_size=128, shuffle='batch')

hdf5Tmp.close() # On peut fermer le fichier temporaire
remove(tmpFile) # et le supprimer

# On évalue le modèle
#score = model.evaluate(X, Y)[1]
#print("Accuracy : " + score)
