inputShape = nbVal * nbCoef # Taille de la première couche : nombre de vecteurs dans une trame * nombre de valeurs dans un vecteur
model = Sequential() # Modèle séquentiel
#Première couche (Entrée)
model.add(Dense(inputShape, input_shape=(inputShape,), kernel_initializer='glorot_normal', activation='relu'))
#Deuxième couche (Cachée)
model.add(Dropout(0.2))
model.add(Dense(256, kernel_initializer='glorot_normal', activation='relu'))
#Trosième couche (Cachée)
model.add(Dropout(0.2))
model.add(Dense(256, kernel_initializer='glorot_normal', activation='relu'))
#Quatrième couche (Sortie)
model.add(Dense(nbSorties, kernel_initializer='glorot_normal', activation='softmax'))

# Les "Dropout" ajoutés sur les couches cachées sont des "mini" couches qui vont ajouter de l'aléatoire dans la sélection des poids à favoriser pour éviter l'apprentissage par coeur
