import cv2, numpy as np
import os, pickle, sys
import calibration.stereo_calib as stercal, calibration.depthMap as depm

CALIB_DIR = '/home/wei/Public/quiXtinguish/data_collection/calibration'

def rectify(left_imsrc, right_imsrc):
    '''
    Captures image from imsrc and returns rectified/undistorted image
    If capturing frames from video, imsrc must be an OpenCV VideoCapture Object
    '''
    limg, rimg = cv2.imread(left_imsrc), cv2.imread(left_imsrc)

    #load calib for stereo rectification
    (lmtx, ldist), (rmtx, rdist), (rot, trans) = depm.load_calib(os.path.join(CALIB_DIR))

    #rectify
    limg, rimg = stercal.sterectify(lmtx, ldist, rmtx, rdist, rot, trans)

    return limg, rimg
