import pretraitement

pretraitement.parseConfig('config.ini')
pretraitement.generateAllMfcc()
pretraitement.convertAllMfccToHdf5()
