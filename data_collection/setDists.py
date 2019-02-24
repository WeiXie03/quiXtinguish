import os
import pickle
import sys

DATA_DIR = './data/gucco'

metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
#load metadata
if os.path.isfile(metadata_path):
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)
else:
    print('metadata not found, aborting')
    sys.exit()

#the following only works with the specific dataset gucco, depth is in meters, target height in cm
for pairNum in range(len(metadata.keys())):
    dep = 0
    tgt_height = 0
    if pairNum in range(11) or pairNum in range(76, 82):
        dep = 250
        if pairNum in range(11):
            tgt_height = 93
        else:
            tgt_height = 15

    elif pairNum in range(11, 39) or pairNum in range(82, 89):
        dep = 300
        if pairNum in range(11, 18):
            tgt_height = 90
        elif pairNum in range(18, 30):
            tgt_height = 37
        elif pairNum in range(30, 39):
            tgt_height = 18
        elif pairNum in range(82, 85):
            tgt_height = 14
        else:
            tgt_height = 89

    elif pairNum in range(39, 53) or pairNum in range(89, 93):
        dep = 400
        if pairNum in range(39, 47):
            tgt_height = 18
        elif pairNum in range(47, 53):
            tgt_height = 31
        else:
            tgt_height = 89

    elif pairNum in range(53, 66) or pairNum in range(93, 96) or pairNum in range(103, 106):
        dep = 500
        if pairNum in range(53, 61):
            tgt_height = 16
        elif pairNum in range(61, 67):
            tgt_height = 47
        elif pairNum in range(93, 96):
            tgt_height = 33
        else:
            tgt_height = 89

    elif pairNum in range(96, 103) or pairNum in range(67, 76):
        dep = 600
        if pairNum in range(96, 100):
            tgt_height = 33
        elif pairNum in range(100, 103):
            tgt_height = 89
        else:
            tgt_height = 16

    elif pairNum in range(106, 112):
        dep = 700
        if pairNum in range(106, 109):
            tgt_height = 33
        else:
            tgt_height = 89

    elif pairNum in range(112, 116) or pairNum in range(138, 144):
        dep = 800
        if pairNum in range(112, 116):
            tgt_height = 89
        else:
            tgt_height = 12

    elif pairNum in range(116, 128):
        dep = 900
        if pairNum in range(116, 120):
            tgt_height = 33
        else:
            tgt_height = 89

    else:
        dep = 1000
        if pairNum in range(129, 133):
            tgt_height = 89
        else:
            tgt_height = 33

    #use pythag to find real depth
    metadata[pairNum]['real depth'] = (dep**2+tgt_height**2)**(1/2)
    metadata[pairNum]['fire height'] = tgt_height

print(metadata)
dec = input('Would you like to save to file?[y/n]: ')
if dec == 'y':
    with open(metadata_path, 'wb') as metadataf:
        metadata = pickle.dump(metadata, metadataf)
else:
    print('aborting')
