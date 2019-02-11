import cv2
import numpy
import pickle
import os
import pdb
import sys

#pdb.set_trace()

class Cam(object):
    def __init__(self, side, img_path):
        self.side = side
        self.win = cv2.namedWindow(self.side, cv2.WINDOW_OPENGL)

        self.img = cv2.imread(img_path) #get img_path from metadata

        #self.supDat = {left:{}, right:{}}


#def saveDat(x, y):
    #saves coordinates of mouse, disparity and calculated depth to json file

if __name__ == "__main__":
    def clicked(event, x, y, flags, (src, metadata)):
        if event == cv2.EVENT_LBUTTONDOWN:
            print('x: ', x, ', y: ', y)
            metadata[src.side]['coords'] = (x, y)
            print('wrote coords to metadata')

    DATA_DIR = 'data/camsSetPerm_channel/'

    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    if os.path.isfile(metadata_path):
        metadataf = open(metadata_path, 'rb')
        metadata = pickle.load(metadataf)
    else:
        print('the file ', metadata_path, ' was not found\nplease terminate this program and run receivewrite2.py')
        sys.exit()
    metadata.sort()

    print(metadata)
    imNum = input('Enter the image number of the left right image pair you would like to use.\n ')
    pair_path = metadata[imNum]

    left = Cam('left', pair_path['left'])
    right = Cam('right', pair_path['right'])

    for src in [left, right]:
        cv2.setMouseCallback(self.side, clicked, (src, metadata))

        cv2.imshow(src.side, src.img)
        while(len(metadata[src.side]) == 1): #should only include image location at this point
            keyHit = cv2.waitKey(1)
            if keyHit == ord('q'):
                break

    def writeIntri(metadata_intri, baseline, focl, disparity, est_depth):
        metadata_intri['baseline'] = baseline
        metadata_intri['focal length'] = focl
        metadata_intri['disparity'] = disparity
        metadata_intri['estimated depth'] = est_depth
        metadata_intri['real depth'] = input('Measure and enter the real distance from the baseline of the camera lenses to the fire target.\t')

        return(metadata_intri)

    CALIB_PATH = "./calibration/camMtx.npy"
    if os.path.isfile(CALIB_PATH)):
        calib = numpy.load(CALIB_PATH)
    focl = calib[4] #focal length y from stereo calibration, refer to https://docs.opencv.org/3.1.0/dc/dbb/tutorial_py_calibration.html
    baseline = float(input('Enter distance between center of camera lenses in cm.\t'))
    disparity = metadata[imNum]['left']['coords'] - metadata[imNum]['right']['coords'] #disparity = left x - right x
    est_depth = (baseline * focl)/disparity
    print('depth of fire is approximately ', est_depth, ' centimeters')

    metadata[imNum] = writeIntri(metadata[imNum], baseline, focl, disparity, est_depth)
    print(metadata)

    pickle.dump(metadata, metadataf)
    metadataf.close()
    cv2.destroyAllWindows()
