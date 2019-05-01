import pickle
import sys

with open(sys.argv[1], 'rb') as metaf:
    metadata = pickle.load(metaf)
    #print(metadata)
    for pair in range(100,202):
        print(pair, metadata[pair])
