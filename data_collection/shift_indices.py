import os, sys, pickle

def load_meta(metapath):
    with open(metapath, 'rb') as metaf:
        metadata = pickle.load(metaf)
        return metadata

if __name__ == "__main__":
    SRC_DIR, DST_DIR = sys.argv[1], sys.argv[2]

    srcmetad = load_meta(os.path.join(SRC_DIR, 'metadata.dat'))
    dstmetad = load_meta(os.path.join(DST_DIR, 'metadata.dat'))

    indshft = len(dstmetad.keys())
    for pairind in range(len(srcmetad.keys())):
        newind = pairind+indshft
        dstmetad[newind] = {}
        for side in 'left', 'right':

            #declare old and new paths, get rid of 'data/'
            #oldpath = os.path.join('ml', srcmetad[pairind][side]['img_path'])
            oldpath = os.path.join(srcmetad[pairind][side]['img_path'])
            #newpath = os.path.join(DST_DIR, side, str(newind) + '.jpg')
            newpath = os.path.join(DST_DIR, '{}_{}.jpg'.format(str(newind), side))

            #move file to dst and rename to change index
            os.renames(oldpath, newpath)
            #update dst metadata
            dstmetad[newind][side] = srcmetad[pairind][side]
            dstmetad[newind][side]['img_path'] = newpath

    dec = input('Would you like to save the new destination metadata?(y/n): ')
    if dec == 'y':
        with open(os.path.join(DST_DIR, 'metadata.dat'), 'wb') as dstmetaf:
            pickle.dump(dstmetad, dstmetaf)

    print('done')
