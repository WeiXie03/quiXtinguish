import pickle
import sys

with open(sys.argv[1], 'rb') as metaf:
    data = pickle.load(metaf)
    for dic in data:
        print(dic, ":", data[dic])
