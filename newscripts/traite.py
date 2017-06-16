import pretraitement

pretraitement.parseConfig('configPerso.ini')
pretraitement.setOS()
#pretraitement.generateAllMfcc()
pretraitement.convertAllMfccToHdf5()
