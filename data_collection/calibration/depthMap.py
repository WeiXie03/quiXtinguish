import numpy
import cv2
from matplotlib import pyplot as plt
import sys, os, pickle
import calibration.stereo_calib as stercal

def load_calib(calib_dir_path):
    #calib dir is directory containing all the calibrated settings

    lDset = numpy.load(os.path.join(calib_dir_path, 'calib_settings_left.npy'))
    rDset = numpy.load(os.path.join(calib_dir_path, 'calib_settings_right.npy'))
    #stereo saved in pickle file
    with open(os.path.join(calib_dir_path, 'calib_settings_stereo.dat'), 'rb') as sterDf:
        sterDset = pickle.load(sterDf)

    #print(len(lDset), len(rDset), len(sterDset))
    return lDset, rDset, sterDset

def gen_dispmap(limg, rimg, mindisp=1, numdisps=256, block=7, speckrange=2, speckwin_size=100):
    '''
    creates disparity map as an ndarray
    input images should already be undistorted
    '''
    #stereo = cv2.StereoBM_create(numDisparities=numdisps, blockSize=block)
    stereo = cv2.StereoSGBM_create(numDisparities=numdisps, blockSize=block, P1=8*4**4, P2=4*8*4**4, disp12MaxDiff=1, uniquenessRatio=10, speckleWindowSize=100, speckleRange=2, mode=True)

    '''
    #set some settings for stereo correspondence algorithm
    stereo.setMinDisparity(mindisp)
    stereo.setSpeckleRange(speckrange)
    stereo.setSpeckleWindowSize(speckwin_size)
    '''

    #compute disparity map
    lgrey, rgrey = cv2.cvtColor(limg, cv2.COLOR_BGR2GRAY), cv2.cvtColor(rimg, cv2.COLOR_BGR2GRAY)
    disparity = stereo.compute(lgrey, rgrey)

    return disparity

if __name__ == "__main__":
    print('enter paths of left then right images then directory containing calibrated settings as command line args')
    limg, rimg = cv2.imread(os.path.join(sys.argv[1])), cv2.imread(os.path.join(sys.argv[2]))
    CALIB_DIR = os.path.join(sys.argv[3])

    DEPTH_VISUALIZATION_SCALE = 2048

    dec = input('are images already undistorted? (y/n): ')
    if dec.lower() == 'n':
    #undistort if necessary
        lDset, rDset, sterDset = load_calib(CALIB_DIR)
        (lmtx, ldist) = lDset[:2]
        (rmtx, rdist) = rDset[:2]
        (rot, trans) = sterDset[:2]

        limg, rimg = stercal.sterectify(lmtx, ldist, rmtx, rdist, rot, trans, limg, rimg)
        print('undistorted')
    else:
        print('continuing')

    #calculate depth map
    depmap = gen_dispmap(limg, rimg)

    #display depth map
    win = cv2.namedWindow('depth map', cv2.WINDOW_AUTOSIZE)
    #cv2.imshow('depth map', depmap / DEPTH_VISUALIZATION_SCALE)
    cv2.imshow('depth map', depmap)
    cv2.waitKey()
