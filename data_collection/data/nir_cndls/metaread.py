import pickle
import sys
import pprint

with open(sys.argv[1], 'rb') as metaf:
    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(pickle.load(metaf))
