# Create first network with Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy

dataFile = sys.argv["1"]

# fix random seed for reproducibility
seed = 7
numpy.random.seed(seed)
# load dataset
dataset = numpy.loadtxt(dataFile, delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:13]
Y = dataset[:,13]
# create model
model = Sequential()
model.add(Dense(390, input_dim=13, init='uniform', activation='relu'))
model.add(Dense(256, init='uniform', activation='relu'))
model.add(Dense(256, init='uniform', activation='relu'))
model.add(Dense(4, init='uniform', activation='sigmoid'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, nb_epoch=150, batch_size=10)
# evaluate the model
#scores = model.evaluate(X, Y)
#print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))