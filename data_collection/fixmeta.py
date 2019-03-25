import os
import pickle
import sys

#DATA_DIR = input('data directory(one level above image directories(left/, right/, NoIR/))\t')
print('enter data directory as command line argument')
DATA_DIR = sys.argv[1]

metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
metadata = None
if os.path.isfile(metadata_path):
    '''with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)'''
    metadata = {}
else:
    print('metadata file not found, aborting')
    sys.exit()

limgs_path = os.path.join(DATA_DIR, 'left/')
print(limgs_path)
rimgs_path = os.path.join(DATA_DIR, 'right/')
nirimgs_path = os.path.join(DATA_DIR, 'NoIR/')

#print('min: ', metadata.keys(), 'max: ', len(os.listdir(limgs_path)))
#for pairNum in range(max(metadata.keys()) + 1, len(os.listdir(limgs_path))):
for pairNum in range(len(os.listdir(limgs_path))):
    metadata[pairNum] = {}

    #left
    limg_path = os.path.join(limgs_path, str(pairNum) + '.jpg')
    print(limg_path)
    metadata[pairNum]['left'] = {'img_path':limg_path}

    #right
    rimg_path = os.path.join(rimgs_path, str(pairNum) + '.jpg')
    metadata[pairNum]['right'] = {'img_path':rimg_path}

    #NIR
    #right
    nirimg_path = os.path.join(nirimgs_path, str(pairNum) + '.jpg')
    metadata[pairNum]['NoIR'] = {'img_path':nirimg_path}

print(metadata)
dec = input('\nWould you like to save the newly modified dataset to the metadata file?[y/n]: ')
if dec == 'y':
    with open(metadata_path, 'wb') as metadataf:
        print(metadataf)
        pickle.dump(metadata, metadataf)
else:
    print('aborting')

