import os, sys, pickle

def load_meta(metapath):
    with open(metapath, 'rb') as metaf:
        metadata = pickle.load(metaf)
    return metadata

if __name__ == "__main__":
    print('enter data directory as command line arg')
    DATA_DIR = sys.argv[1]

    metadata = load_meta(os.path.join(DATA_DIR, 'metadata.dat'))

    for pairnum in range(len(metadata.keys())):
        for side in 'left', 'right':
            metadata[pairnum][side]['coords'] = None

    print(metadata[len(metadata.keys())-10])
    dec = input('done, save updated metadata?(y/n): ')
    if dec.lower() == 'y':
        with open(os.path.join(DATA_DIR, 'metadata.dat'), 'wb') as metaf:
            metadata = pickle.dump(metadata, metaf)
        print('saved')
    else:
        print('aborted')
