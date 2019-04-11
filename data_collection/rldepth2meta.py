import os, sys, pickle, pprint
import numpy

def ins_meta(rldepth, fire_height, ind, metadata):
    metadata[ind]['real depth'] = rldepth
    metadata[ind]['fire height from ground'] = fire_height
    pprint.pprint(metadata[ind])

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    sprdsht_path = os.path.join(DATA_DIR, 'distances_for_proc.csv')

    print('please backup your metadata first')
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)

    dat = numpy.loadtxt(sprdsht_path, delimiter=",")
    #dat will be a 2d array, with each subarray as a row
    for row in dat:

        #assign the three columns for each row
        ind = row[0]
        depth = row[1]
        fireh = row[2]

        ins_meta(depth, fireh, ind, metadata)

    pprint.pprint(metadata)
    dec = input('Would you like to save to file?[y/n]: ')
    if dec == 'y':
        with open(metadata_path+'2', 'wb') as metadataf:
            pickle.dump(metadata, metadataf)
        print('saved to', metadata_path+'2')
    else:
        print('okie')
