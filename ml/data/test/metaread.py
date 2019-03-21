import pickle

with open('./metadata.dat', 'rb') as metaf:
    print(pickle.load(metaf))
