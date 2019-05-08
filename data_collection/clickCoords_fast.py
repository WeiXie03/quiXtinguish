import cv2
import numpy as np
import os, sys, pickle
import pprint
import pdb
from calibration import stereo_calib as stercal

#pdb.set_trace()
CLICKED = False

class Camera(object):
    def __init__(self, side):
        self.side = side
        #orig image size should be 640x480, scale up by 2.15x in both x and y
        self.img = None

def clicked(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        src = param[1]
        coord_dict = param[0]
        print('x: ', x, ', y: ', y)
        coord_dict["x"] = x
        coord_dict["y"] = y
        print('selected')

        #draw cross to mark click
        disp_img = cv2.drawMarker(src.img.copy(), (x,y), (214, 126, 12), cv2.MARKER_CROSS, 15, 1)
        cv2.imshow('click labeler', disp_img)
        global CLICKED
        CLICKED = True

def waitClick(src):
    print('waiting click')
    coord_dict = {'x':None, 'y':None}
    cv2.setMouseCallback('click labeler', clicked, (coord_dict, src))
    print('hit space to confirm your selection, q at any time to exit')
    while True:
        key = cv2.waitKey(1)
        global CLICKED
        if(key == 32 and CLICKED):
            CLICKED = False
            break
        elif(key == ord('q')):
            return None, None
        elif(key == ord('s')):
            return 'skip', 'skip'
    return coord_dict['x'], coord_dict['y']

def load_calib(calib_path):
    (lmtx, ldist) = np.load(os.path.join(calib_path, 'calib_settings_left.npy'))[:2]
    (rmtx, rdist) = np.load(os.path.join(calib_path, 'calib_settings_right.npy'))[:2]
    (rot, trans) = np.load(os.path.join(calib_path, 'calib_settings_stereo.dat'))[:2]

    return lmtx, rmtx, ldist, rdist, rot, trans

if __name__ == "__main__":
    print('data directory is command line argument after this python program\'s name')
    DATA_DIR = sys.argv[1]
    CALIB_DIR = sys.argv[2]

    lmtx, rmtx, ldist, rdist, rot, trans = load_calib(CALIB_DIR)

    #load the metadata
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    metadata = None
    if os.path.isfile(metadata_path):
        with open(metadata_path, 'rb') as metadataf:
            metadata = pickle.load(metadataf)
    else:
        print('the file ', metadata_path, ' was not found\nplease run receivewrite2.py')
        sys.exit()

    #save backup
    with open(metadata_path+'e', 'wb') as metadataf:
        pickle.dump(metadata, metadataf)

    #get the image pair the user wants
    left = Camera('left')
    right = Camera('right')

    #make window to display images
    win = cv2.namedWindow('click labeler', cv2.WINDOW_AUTOSIZE)

    pprint.pprint(metadata[0])
    print('\n', 3*'\t', '...\n')
    pprint.pprint(metadata[len(metadata.keys())-1])

    imNum = None
    done = False
    for src in left, right:
        for imNum in metadata.keys():
        #for imNum in range(0, 47+1):
            #metadata[imNum][src.side]['coords'] = ()

            img_path = metadata[imNum][src.side]['img_path']
            #save first of consecutive frames as image for each camera
            src.img = cv2.imread(os.path.join(img_path)) #get img_path from metadata

            #numFires = int(input('Enter the number of fires in the image pair: '))
            numFires = 1
            #print('hit any key to continue')

            print('Click on a fire in the image. When you are done, a window will pop up for you to select the corresponding point on the other image.')
            for index in range(numFires):

                #enlargen image for easier clicking
                xscale, yscale = 2, 2
                src.img = cv2.resize(src.img, None, fx=xscale, fy=yscale, interpolation=cv2.INTER_CUBIC)
                #load image into window, get number of fires from user
                cv2.imshow('click labeler', src.img)

                mx, my = waitClick(src)
                if mx is None:
                    done = True
                    print("Done")
                    break
                elif mx == 'skip':
                    metadata[imNum][src.side]['coords'] = (None, None)
                    print(metadata[imNum], 'skipping')
                    continue
                #store coordinates for every image
                #paird[src.side]['coords'][index] = (mx, my)
                metadata[imNum][src.side]['coords'] = (mx/xscale, my/yscale)
                print(metadata[imNum])

                with open(metadata_path, 'wb') as metadataf:
                    pickle.dump(metadata, metadataf)

            if done:
                break
            pprint.pprint(metadata[imNum])

    pprint.pprint(metadata)
    if input('Would you like to save to file?[y/n]: ') == 'y':
        with open(metadata_path, 'wb') as metadataf:
            pickle.dump(metadata, metadataf)
    else:
        print('aborting')
    cv2.destroyAllWindows()
