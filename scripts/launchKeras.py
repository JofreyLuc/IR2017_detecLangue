# Crée un réseau de neurones avec Keras

from keras.models import Sequential
from keras.layers import Dense
from keras.utils.np_utils import to_categorical
import numpy
import sys

#On récupère les données
dataFile = sys.argv[1]

#On charge les données (dans un tableau numpy actuellement)
dataset = numpy.loadtxt(dataFile, delimiter=",")

#On divise les données en séparant leur étiquette
X = dataset[:,0:13]
Y = dataset[:,13]
Y = to_categorical(Y)

#On crée le modèle séquentiel, avec 4 couches
model = Sequential()
model.add(Dense(390, input_dim=13, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(256, kernel_initializer='normal', activation='relu'))
model.add(Dense(4, kernel_initializer='normal', activation='sigmoid'))

#On compile le modèle
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

#On entraîne le modèle
model.fit(X, Y, epochs=10, batch_size=10)

#On évalue le modèle
score = model.evaluate(X, Y)[1]
print("Accuracy : " + score)
