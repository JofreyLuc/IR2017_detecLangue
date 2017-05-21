# Crée un réseau de neurones avec Keras

from keras.models import Sequential
from keras.layers import Dense, Dropout
import numpy as np
import h5py
import sys
from os import remove, path
from glob import glob
import matplotlib.pyplot as plt

# Paramètres
#Affichage du traitement des données
AFFICHAGE = True
# Nombre de coefficients cepstraux
nbCoef = 13
# Nombre de valeurs à prélever pour obtenir une "fenêtre de parole"
nbVal = 101
# Décalage entre chaque prélevement de fenêtre de parole
shift = 5
#Nombre de langages différents = de neurones en sortie
nbSorties = 4

def formatDataMemory(dataFileName, withoutLabel=False):
    '''
    Formatte les données d'un fichier hdf5 qui est organisé en plusieurs datasets
    qui contiennent chacun des fenêtres de parole en deux tableaux numpy (données et étiquettes)
    lisibles par Keras.
    :param dataFile: Le fichier hdf5 d'entrée.
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

    X = np.zeros([totalFrames, nbVal * nbCoef], dtype=np.float32)
    Y = np.zeros([totalFrames, nbSorties], dtype=np.float32)
    # On va stocker les valeurs de la fenêtre de parole dans un tableau numpy temporaire
    frameValues = np.zeros([nbVal * nbCoef], dtype=np.float32)
    frameIndex = 0
    # Parcours des datasets du fichier d'entrée afin de remplir les datasets temporaires
    for dataset in hdf5In.values():
        if AFFICHAGE : print('Traitement de ' + dataset.name)
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
                vectorIndex += nbCoef  # au fur et à mesure

            # On remplit les tableaux numpy avec les données et le langage
            X[frameIndex] = frameValues
            if not withoutLabel:
                Y[frameIndex, int(language)] = 1
            frameIndex += 1

    hdf5In.close()
    
    if withoutLabel:
        return X
    else:
        return (X, Y)

# Calcule la variance de chaque coeff mfcc 
def calculateVariances(dataFileName):
    hdf5In = h5py.File(dataFileName, "r")
    
    nbValue = 0
    averages = np.zeros([nbCoef], dtype=np.float32)
    for dataset in hdf5In.values():                             # Pour chaque dataset du fichier hdf5
        print(dataset)
        nbValue += dataset.shape[0]
        for mfccArray in dataset:
            averages += mfccArray[:nbCoef]
    averages /= nbValue  # calcul moyenne
    
    variances = np.zeros([nbCoef], dtype=np.float32)
    for dataset in hdf5In.values():                             # Pour chaque dataset du fichier hdf5
        print(dataset)
        for mfccArray in dataset:
            variances += (mfccArray[:nbCoef] - averages)**2
    variances /= nbValue
    
    return variances
        
if __name__ == '__main__':
    # On récupère les données
    dataFileName = sys.argv[1]
    devFileName = sys.argv[2]
    testFileName = sys.argv[3]
    
    # On formatte les données
    (X, Y) = formatDataMemory(dataFileName)
    (Xdev, Ydev) = formatDataMemory(devFileName)
    (Xtest, Ytest) = formatDataMemory(testFileName)

    # On calcule la variance de chaque coefficient mfcc
    # variances obtenues à l'aide de la fonction calculateVariances
    variances = [ 8.44184971,  3.82373691,  2.00800991,  1.17921674,  1.13604367,  0.72418207,  0.55174363,  0.44808063,  0.40456247,  0.30078402,  0.27061722,  0.24347636, 0.05386801]
    #calculateVariances(dataFileName)

    # On concatène nbVal fois le tableau de variances afin de pouvoir effectuer la division en une seule fois
    variancesDuplicate = []
    for i in range(nbVal): variancesDuplicate[i*nbVal:] = variances
    # et on divise chaque coefficient mfcc du train et du dev par sa variance
    X /= variancesDuplicate
    Xdev /= variancesDuplicate

    # On crée le modèle séquentiel, avec 4 couches
    inputShape = nbVal * nbCoef
    model = Sequential()
    model.add(Dense(inputShape, input_shape=(inputShape,), kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(256, kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(256, kernel_initializer='glorot_normal', activation='relu'))
    model.add(Dense(nbSorties, kernel_initializer='glorot_normal', activation='softmax'))

    # On compile le modèle
    model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

    # On entraîne le modèle
    history = model.fit(X, Y, epochs=100, batch_size=128, validation_data=(Xdev, Ydev))
    
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['dev'], loc='upper left')
    plt.savefig('testDropout101_5.png')

    # Crée un fichier avec les probabilités résultat
    #generatePredict(model, 'hdf5Predict/Arabic', 'Arabic')
    #generatePredict(model, 'hdf5Predict/English', 'English')
    #generatePredict(model, 'hdf5Predict/French', 'French')
    #generatePredict(model, 'hdf5Predict/German', 'German')
    
