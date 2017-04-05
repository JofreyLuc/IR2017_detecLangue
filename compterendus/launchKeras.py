# Crée un réseau de neurones avec Keras

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
import numpy as np
import h5py
import sys
from os import remove

def formatDataForKeras(dataFileName, hdf5Tmp, nbVal, nbCoef, shift, withoutLabel=False):
    '''
    Formatte les données d'un fichier hdf5 qui est organisé en plusieurs datasets
    qui contiennent chacun des fenêtres de parole en deux tableaux numpy (données et étiquettes)
    lisibles par Keras.
    :param dataFile: Le fichier hdf5 d'entrée.
    :param hdf5Tmp: Le fichier hdf5 contenant les donnée structurées
    :param nbVal: Le nombre de valeurs à prélever pour obtenir une "fenêtre de parole"
    :param nbCoef: Les nombre de coefficient par vecteur acoustique
    :param shift: Le décalage entre chaque fenêtre de parole
    :param withoutLabel:Permet de spécifier que les données ne sont pas étiquettées 
    '''
    hdf5In = h5py.File(dataFileName, "r")
    
    # Calcul du nombre total de fenêtres de parole de la base d'apprentissage
    # Une fenêtre est une matrice contenant des coefficients cepstraux :
    # - de nbVal lignes 
    # - de nbCoef colonnes
    totalFrames = 0
    for dataset in hdf5In.values():                             # Pour chaque dataset du fichier hdf5
        frames = int ((dataset.shape[0] - nbVal) / shift) + 1   # Nb fenêtres du dataset
        totalFrames += frames
    
    # On places les datasets générés par cette fonction dans des groupes nommés de 1 à n
    groupLastName = 0
    for groupName in hdf5Tmp:
        groupLastName = groupName
    newGroupName = str(int(groupLastName) + 1)
    # Création des datasets contenant les données formatées
    hdf5Tmp.create_dataset(newGroupName+"/examples", (totalFrames, nbVal * nbCoef)) # dataset données
    X = hdf5Tmp.get(newGroupName+"/examples")
    if not withoutLabel:
        hdf5Tmp.create_dataset(newGroupName+"/languages", (totalFrames,))           # dataset étiquettes
        Y = hdf5Tmp.get(newGroupName+"/languages")

    # On va stocker les valeurs de la fenêtre de parole dans un tableau numpy temporaire
    # cela permet d'accélerer le remplissage des datasets temporaires
    frameValues = np.empty([nbVal * nbCoef])
    frameIndex = 0
    # Parcours des datasets du fichier d'entrée afin de remplir les datasets temporaires
    for dataset in hdf5In.values():
        print(dataset)
        # On prend chaque fenêtre de parole du dataset courant
        for frameStartIndex in range(0, len(dataset) - nbVal, shift):
            # Une fenêtre de nbVal vecteurs
            frameVectors = dataset[frameStartIndex : frameStartIndex + nbVal]
            # On prend le langage sur le premier vecteur de la fenêtre (dernière valeur du vecteur)
            if not withoutLabel:
                language = frameVectors[0][len(frameVectors[0])-1]
            vectorIndex = 0
            # Pour chaque vecteur (contenant nbCoef valeurs) de la fenêtre courante
            for vector in frameVectors :
                # On remplit le tableau de la fenêtre de parole avec les coefficients du vecteur
                frameValues[vectorIndex : vectorIndex + nbCoef] = vector[0 : nbCoef]
                vectorIndex += 13  # au fur et à mesure

            # On remplit le dataset data avec les coefficients du vecteur
            X[frameIndex] = frameValues
            if not withoutLabel:
                Y[frameIndex] = language
            frameIndex += 1

    hdf5In.close()
    
    if withoutLabel:
        return X
    else:
        Y = to_categorical(Y)   # On met les étiquettes sous forme de vecteurs binaires pour keras
        return (X, Y)

if __name__ == '__main__':   
    # Paramètres
    # Nombre de coefficients cepstraux
    nbCoef = 13
    # Nombre de valeurs à prélever pour obtenir une "fenêtre de parole"
    nbVal = 31
    # Décalage entre chaque prélevement de fenêtre de parole
    shift = 10

    # On récupère les données
    dataFileName = sys.argv[1]
    devFileName = sys.argv[2]
    testFileName = sys.argv[3]
    # On crée le fichier temporaire hdf5
    tmpFile = "tmp.hdf5"
    hdf5Tmp = h5py.File(tmpFile, "w")

    # On formatte les données
    (X, Y) = formatDataForKeras(dataFileName, hdf5Tmp, nbVal, nbCoef, shift)
    (Xdev, Ydev) = formatDataForKeras(devFileName, hdf5Tmp, nbVal, nbCoef, shift)
    (Xtest, Ytest) = formatDataForKeras(testFileName, hdf5Tmp, nbVal, nbCoef, shift)

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
    model.fit(X, Y, epochs=10, batch_size=128, validation_data=(Xdev, Ydev), shuffle='batch')

    hdf5Tmp.close() # On peut fermer le fichier temporaire
    remove(tmpFile) # et le supprimer

    # On évalue le modèle
    #score = model.evaluate(Xtest, Ytest)[1]
    #print("Accuracy : " + score)
