import cv2, numpy as np
import os, pickle, sys, shutil
from calibration import stereo_calib as stercal, depthMap as depm

def load_meta(data_dir_path):
    with open(os.path.join(data_dir_path, 'metadata.dat'), 'rb') as metaf:
        metadata = pickle.load(metaf)
    return metadata

if __name__ == "__main__":
    print('enter path of data directory, then calibration settings directory')
    DATA_DIR, CALIB_DIR = sys.argv[1], sys.argv[2]

    #load calibrated settings for undistorting
    lDset, rDset, sterDset = depm.load_calib(CALIB_DIR)

    #make directory inside current data dir to store undistorted images
    undist_dir = os.path.join(DATA_DIR, 'undistorted')
    os.mkdir(undist_dir)
    new_metadata = {}

    og_metadata = load_meta(DATA_DIR)
    #loop through metadata entries
    for pairind in range(len(og_metadata.keys())):

        limg_path = os.path.join(og_metadata[pairind]['left']['img_path'])
        rimg_path = os.path.join(og_metadata[pairind]['right']['img_path'])
        #load orig images
        limg, rimg = cv2.imread(limg_path), cv2.imread(rimg_path)

        #undistort images
        limg, rimg = stercal.sterectify(lDset[0], lDset[1], rDset[0], rDset[1], sterDset[0], sterDset[1], limg, rimg)

        #save new images
        limg_path = os.path.join(undist_dir, str(pairind)+'_left.jpg')
        cv2.imwrite(limg_path, limg)
        rimg_path = os.path.join(undist_dir, str(pairind)+'_right.jpg')
        cv2.imwrite(rimg_path, rimg)
        print('saved undistorted image pair {}'.format(pairind))

        #make entries in metadata
        new_metadata[pairind] = {}
        new_metadata[pairind]['left'] = {}
        new_metadata[pairind]['left']['img_path'] = limg_path

        new_metadata[pairind]['right'] = {}
        new_metadata[pairind]['right']['img_path'] = rimg_path

    #save metadata
    print('saving metadata')
    newmeta_path = os.path.join(undist_dir, 'metadata.dat')
    with open(newmeta_path, 'wb') as metaf:
        pickle.dump(new_metadata, metaf)

    print('done')
