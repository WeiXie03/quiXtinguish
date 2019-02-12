import os
import pickle
import sys

DATA_DIR = './'

metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
metadata = None
if os.path.isfile(metadata_path):
    metadataf = open(metadata_path, 'r+b')
    metadata = pickle.load(metadataf)
    #metadata = {}
else:
    print('metadata file not found, aborting')
    sys.exit()

limgs_path = os.path.join(DATA_DIR, 'left/')
rimgs_path = os.path.join(DATA_DIR, 'right/')

#print('min: ', metadata.keys(), 'max: ', len(os.listdir(limgs_path)))
for pairNum in range(max(metadata.keys()) + 1, len(os.listdir(limgs_path))):
#for pairNum in range(len(os.listdir(limgs_path))):
    #left
    limg_path = os.path.join(limgs_path, str(pairNum), '.jpg')
    metadata[pairNum] = {'left':{'img_path':limg_path}}

    #right
    rimg_path = os.path.join(rimgs_path, str(pairNum), '.jpg')
    metadata[pairNum] = {'right':{'img_path':rimg_path}}
print(metadata)
dec = input('\nWould you like to save the newly modified dataset to the metadata file?[y/n]: ')
if dec == 'y':
    pickle.dump(metadata, metadataf)
else:
    print('aborting')

metadataf.close()
