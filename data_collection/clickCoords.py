import cv2
import numpy as np
import pickle
import pdb
import os
import sys

#pdb.set_trace()

class Camera(object):
    def __init__(self, side):
        self.side = side
        self.win = cv2.namedWindow(self.side, cv2.WINDOW_AUTOSIZE)
        self.img = None

def clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        src = param[1]
        coord_dict = param[0]
        print('x: ', x, ', y: ', y)
        coord_dict["x"] = x
        coord_dict["y"] = y
        print('selected')
        disp_img = cv2.circle(src.img, (x,y), 4, (0,14,231), 1)
        cv2.imshow(src.side, disp_img)

def waitClick(src):
    print('waiting click')
    coord_dict = {'x':None, 'y':None}
    cv2.setMouseCallback(src.side, clicked, (coord_dict, src))
    print('hit space to confirm your selection, q at any time to exit')
    while True:
        key = cv2.waitKey(1)
        if(key == 32):
            break
        elif(key == ord('q')):
            sys.exit()
    return coord_dict['x'], coord_dict['y']

if __name__ == "__main__":
    print('data directory is command line argument after this python program\'s name')
    DATA_DIR = sys.argv[1]

    #load the metadata
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    metadata = None
    if os.path.isfile(metadata_path):
        with open(metadata_path, 'rb') as metadataf:
            metadata = pickle.load(metadataf)
    else:
        print('the file ', metadata_path, ' was not found\nplease run receivewrite2.py')
        sys.exit()

    #get the image pair the user wants
    left = Camera('left')
    right = Camera('right')
    nir = Camera('NoIR')

    print(metadata)

    imNum = None
    while(True):
        imNum = (input('Enter the image number you would like to use or\nEnter \'w\' if you would like to finish and save to file.\n')
)
    #for imNum in range(76, len(metadata.keys())):
        if imNum == 'w':
            break
        imNum = int(imNum)

        paird = metadata[imNum]

        for src in (left, right, nir):
            paird[src.side]['coords'] = {}

            img_path = paird[src.side]['img_path']
            src.img = cv2.imread(img_path) #get img_path from metadata

        #print('Look at how many fires there are.')
        #cv2.imshow("both", np.hstack((left.img[::2, ::2],right.img[::2, ::2])))
        #cv2.waitKey(500)

        #numFires = int(input('Enter the number of fires in the image pair: '))
        numFires = 1
        #print('hit any key to continue')

        print('Click on a fire in the image. When you are done, a window will pop up for you to select the corresponding point on the other image.')
        for index in range(numFires):
            for src in (left, right, nir):
                #create new image field of wrappers

                #load image into window, get number of fires from user
                cv2.imshow(src.side, src.img)
                mx,my = waitClick(src)
                #store coordinates as values to index keys, will store points of corresponding left right images with same key
                paird[src.side]['coords'][index] = (mx, my)

        metadata[int(imNum)] = paird
        print(paird)

        #save to duplicate
        with open(metadata_path+'e', 'wb') as metadataf:
            pickle.dump(metadata, metadataf)

    '''
        def writeIntri(metadata_intri, baseline, focl, disparity, est_depth):
            metadata_intri['baseline'] = baseline
            metadata_intri['focal length'] = focl
            metadata_intri['disparity'] = disparity
            metadata_intri['estimated depth'] = est_depth
            metadata_intri['real depth'] = input('Measure and enter the real distance from the baseline of the camera lenses to the fire target.\t')

            return(metadata_intri)

        CALIB_PATH = "./calibration/camMtx.npy"
        if os.path.isfile(CALIB_PATH):
            calib = np.load(CALIB_PATH)
        focl = calib[4] #focal length y from stereo calibration, refer to https://docs.opencv.org/3.1.0/dc/dbb/tutorial_py_calibration.html
        baseline = float(input('Enter distance between center of camera lenses in cm.\t'))
        disparity = metadata[imNum]['left']['coords'] - metadata[imNum]['right']['coords'] #disparity = left x - right x
        est_depth = (baseline * focl)/disparity
        print('depth of fire is approximately ', est_depth, ' centimeters')

        metadata[imNum] = writeIntri(metadata[imNum], baseline, focl, disparity, est_depth)

    '''
    print(metadata)
    if input('Would you like to save to file?[y/n]: ') == 'y':
        with open(metadata_path, 'wb') as metadataf:
            pickle.dump(metadata, metadataf)
    else:
        print('aborting')
    cv2.destroyAllWindows()
