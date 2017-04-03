# Crée un réseau de neurones avec Keras

from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils.np_utils import to_categorical
import numpy as np
import h5py
import sys

#On récupère les données
dataFile = sys.argv[1]
hdf5In = h5py.File(dataFile, "r")

debut = True

lala = 0

#Pour chaque dataset du fichier hdf5
for dataset in hdf5In.values():
    interval = 31
    shift = 10
    count = 0
    for index in range(0, len(dataset) - interval, shift):
        values = dataset[index:index+interval]
        language = values[0][13] #13 en dur
        datasetValues = []
        for i in values :
            datasetValues = np.concatenate((datasetValues, i[0:13]), axis=0)

        if debut :
            examplesArray = np.array([datasetValues])
            languagesArray = np.array([language])
            debut = False
        else :
            examplesArray = np.append(examplesArray, [datasetValues], axis=0)
            languagesArray = np.append(languagesArray, [language], axis=0)
            
#On divise les données en séparant leur étiquette
#X = dataset[:,0:13]
#Y = dataset[:,13]

languagesArray = to_categorical(languagesArray)

#On crée le modèle séquentiel, avec 4 couches
model = Sequential()
#model.add(Dropout(0.2, input_shape=(13,)))
model.add(Dense(403, input_shape=(403,), kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(2, kernel_initializer='normal', activation='softmax'))

#On compile le modèle
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

#On entraîne le modèle
model.fit(examplesArray, languagesArray, epochs=500, validation_split=0.1, batch_size=128)

#On évalue le modèle
#score = model.evaluate(X, Y)[1]
#print("Accuracy : " + score)