import os, sys
import pickle, csv

def load_inds(sprdsht_f):
    '''get index of first image of each height and depth configuration'''
    inds = []
    data = csv.reader(sprdsht_f)
    for row in data:
        inds.append(int(row[0]))
    return inds

def fill_newmeta(old_metad, des_inds):
    newmetad = {}
    for newind, desind in enumerate(des_inds):
        newmetad[newind] = old_metad[desind]
    return newmetad

if __name__ == "__main__":
    sprdsht_fpath = os.path.join(sys.argv[1])
    meta_fpath = os.path.join(sys.argv[2])

    with open(sprdsht_fpath, 'r') as sprdsht_f:
        des_inds = load_inds(sprdsht_f)

    with open(os.path.join(meta_fpath), 'rb') as oldmeta_f:
        oldmetad = pickle.load(oldmeta_f)

    with open(os.path.join('.', 'crpd_metadata.dat'), 'w+b') as new_metaf:
        newmetad = fill_newmeta(oldmetad, des_inds)

        print('new metadata\n', newmetad)
        dec = input('save?(y/n): ')
        if dec.lower() == 'y':
            pickle.dump(newmetad, new_metaf)
            print('done')
        else:
            print('aborted')
