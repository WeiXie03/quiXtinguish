import pickle, os, sys

with open(os.path.join(sys.argv[1]), 'rb') as f:
    data = pickle.load(f)
    print(data)
