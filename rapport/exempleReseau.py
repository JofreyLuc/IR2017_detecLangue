model = Sequential()                         # creation d'un modele sequentiel
model.add(Dense(units=64, input_dim=100))    # ajout d'une couche
model.add(Activation('relu'))                # et de sa fonction d'activation

# permet de configurer differents parametres de la phase d'apprentissage du reseau
model.compile(loss='categorical_crossentropy', optimizer='sgd', metrics=['accuracy'])                              

# lance la phase d'apprentissage sur 5 epochs
model.fit(x_train, y_train, epochs=5, batch_size=32)
