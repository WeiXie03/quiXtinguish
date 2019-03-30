import pickle
import sys

with open(sys.argv[1], 'rb') as metaf:
    print(pickle.load(metaf))
