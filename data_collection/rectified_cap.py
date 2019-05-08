import cv2, numpy as np
import os, pickle, sys
import calibration.stereo_calib as stercal
import calibration.depthMap as depm

def rectify(left_imsrc, right_imsrc, calib_path):
    '''
    Captures image from imsrc and returns rectified/undistorted image
    imsrc must be image read by opencv(a mat), will change to accomodate live video in the future
    '''
    limg, rimg = left_imsrc, right_imsrc

    #load calib for stereo rectification
    calib_data = depm.load_calib(os.path.join(calib_path))
    (lmtx, ldist), (rmtx, rdist), (rot, trans) = calib_data[0][:2], calib_data[1][:2], calib_data[2][:2]

    #rectify
    limg, rimg = stercal.sterectify(lmtx, ldist, rmtx, rdist, rot, trans, limg, rimg)

    return limg, rimg
