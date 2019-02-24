import numpy
import os
import pickle
import sys
import matplotlib.pyplot as plt
import math

DATA_DIR = './data/gucco'

metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
#load metadata
if os.path.isfile(metadata_path):
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)
else:
    print('metadata not found, aborting')
    sys.exit()

errs = []
dists = []
disp = []
for pairNum in range(77, len(metadata.keys())):
    dist = metadata[pairNum]['real depth']
    dists.append(dist)
    err = math.fabs(metadata[pairNum]['estimated depth'] - dist)
    errs.append(err)
    disp.append(metadata[pairNum]['left']['coords'][0][0]-metadata[pairNum]['right']['coords'][0][0])

print('errors in cm ', errs, ', distances ', dists)
#plt.plot(dists, errs,'ro')
print(disp)
plt.plot(dists, disp,'ro')
plt.show()
