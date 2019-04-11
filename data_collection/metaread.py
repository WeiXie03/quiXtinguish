import pickle, pprint
import sys

with open(sys.argv[1], 'rb') as metaf:
    pprint.pprint(pickle.load(metaf))
