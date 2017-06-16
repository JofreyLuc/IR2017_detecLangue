import pretraitement

pretraitement.setOS()
pretraitement.parseConfig('configPerso.ini')
pretraitement.generateAllMfcc()
pretraitement.convertAllMfccToHdf5()
