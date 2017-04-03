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

#Pour chaque dataset du fichier hdf5
for dataset in hdf5In.values():
    language = dataset[:,13][0]
    interval = 31
    shift = 10
    count =0
    datasetValues = []
    for index in range(0, len(dataset) - interval, shift):
        values = dataset[index:index+interval]
        language = values[0][13]
        for i in range(len(values)):
            for j in range(len(values[0])):
                datasetValues.append(dataset[i][j])
    print(datasetValues)
exit()
#On divise les données en séparant leur étiquette
X = dataset[:,0:13]
Y = dataset[:,13]

Y = to_categorical(Y)

#On crée le modèle séquentiel, avec 4 couches
model = Sequential()
#model.add(Dropout(0.2, input_shape=(13,)))
model.add(Dense(13, input_shape=(13,), kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(2, kernel_initializer='normal', activation='softmax'))

#On compile le modèle
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

#On entraîne le modèle
model.fit(X, Y, epochs=500, validation_split=0.1, batch_size=128)

#On évalue le modèle
#score = model.evaluate(X, Y)[1]
#print("Accuracy : " + score)
