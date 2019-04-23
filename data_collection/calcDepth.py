import os, sys, pickle
import cv2, numpy

#NOTE: this program is DEPRECATED, calculating depth in plt_stereo_err

def load_meta(metapath):
    with open(os.path.join(metapath), 'rb') as metaf:
        metadata = pickle.load(metaf)
    return metadata

def load_foclx(calib_path):
    '''
    Averages x focal length of left and right cameras stored in calibrated settings
    '''
    lcalib = numpy.load(os.path.join(calib_path, 'calib_settings_left.npy'))
    rcalib = numpy.load(os.path.join(calib_path, 'calib_settings_right.npy'))

    foclx = (lcalib[0][0][0] + rcalib[0][0][0])/2
    return foclx

def estdepth(baseline, foclx, lcoords, rcoords):
    lx, rx = lcoords[0], rcoords[0]
    estdepth = (baseline*foclx)/(lx-rx)
    return estdepth

if __name__ == "__main__":
    print('enter path of data directory, then calibration (settings) directory as command line args')
    DATA_DIR = sys.argv[1]
    CALIB_DIR = sys.argv[2]

    #straight-line distance between optical centers
    BASELINE = float(input('Distance between cameras in cm: '))

    metadata = load_meta(os.path.join(DATA_DIR, 'metadata.dat'))

    for pairind in len(metadata.keys()):
        paird = metadata[pairind]
    #...
