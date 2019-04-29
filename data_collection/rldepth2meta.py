import os, sys, pickle, pprint
import csv

def ins_meta(rldepth, fire_height, ind, metadata):
    metadata[ind]['real depth'] = rldepth
    metadata[ind]['fire height from ground'] = fire_height
    #pprint.pprint(metadata[ind])

if __name__ == "__main__":
    DATA_DIR = sys.argv[1]
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    sprdsht_path = os.path.join(DATA_DIR, 'distances_for_proc.csv')

    print('please backup your metadata first')
    with open(metadata_path, 'rb') as metadataf:
        metadata = pickle.load(metadataf)

    with open(sprdsht_path) as sprdshtf:
        reader = csv.reader(sprdshtf, delimiter=',')

        #dat will be a 2d array, with each subarray as a row
        for row in reader:
            #NOTE: spreadsheet should NOT have column headers

            #assign the three columns for each row
            start = int(row[0])
            end = int(row[1])
            depth = float(row[2])
            fireh = float(row[3])
            print(fireh)

            for ind in range(start, end+1):
                ins_meta(depth, fireh, ind, metadata)

    print('\n')
    #pprint.pprint(metadata)
    dec = input('Would you like to save to file?[y/n]: ')
    if dec == 'y':
        with open(metadata_path, 'wb') as metadataf:
            pickle.dump(metadata, metadataf)
        print('saved to', metadata_path)
    else:
        print('okie')
