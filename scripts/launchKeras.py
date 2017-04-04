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

#création d'un fichier hdf5 temporaire
hdf5Out = h5py.File("tmp.hdf5", "w")

#Nombre d'exemples
totalFrames = 0
for dataset in hdf5In.values():
    frames = int((dataset.shape[0]-31)/10)+1
    totalFrames+=frames




totalFrames *= 20
print(totalFrames)



hdf5Out.create_dataset("examples", (totalFrames, 13*31))
hdf5Out.create_dataset("languages", (totalFrames,))

examplesArray = hdf5Out.get("examples")
languagesArray = hdf5Out.get("languages")

debut = True
#examplesArray = np.empty([totalFrames, 13*31])
#languagesArray = np.empty([totalFrames])
interval = 31
shift = 10
count = 0

#Pour chaque dataset du fichier hdf5
for j in range(20):
    print(j)
    for dataset in hdf5In.values():
        #print(dataset)


        for index in range(0, len(dataset) - interval, shift):
            values = dataset[index:index+interval]
            language = values[0][13] #13 en dur
            datasetValues = np.empty([13*31])
            count0=0
            for i in values :
                #datasetValues = np.concatenate((datasetValues, i[0:13]), axis=0)
                datasetValues[count0:count0+13] = i[0:13]
                count0 += 13

            examplesArray[count] = datasetValues
            languagesArray[count] = language
            count+=1

languagesArray = to_categorical(languagesArray)

#On crée le modèle séquentiel, avec 4 couches
model = Sequential()
#model.add(Dropout(0.2, input_shape=(13,)))
model.add(Dense(403, input_shape=(403,), kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(4, kernel_initializer='normal', activation='softmax'))

#On compile le modèle
model.compile(loss='categorical_crossentropy', optimizer='RMSprop', metrics=['accuracy'])

#On entraîne le modèle
model.fit(examplesArray, languagesArray, epochs=10, batch_size=128, shuffle='batch')

#On évalue le modèle
#score = model.evaluate(X, Y)[1]
#print("Accuracy : " + score)
