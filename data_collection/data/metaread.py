import pickle
import pprint
import sys

pp = pprint.PrettyPrinter(indent=4)

with open(sys.argv[1], 'rb') as metaf:
    pp.pprint(pickle.load(metaf))
