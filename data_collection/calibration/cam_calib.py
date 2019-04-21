import cv2, numpy
import os, sys, pickle
import argparse

def argp_init():
    parser = argparse.ArgumentParser(description="Calibrate two cameras for stereo vision using checkerboard pattern.")
    parser.add_argument('data_dir', type=str, nargs=1, help='directory containing stereo images of pattern')
    parser.add_argument('calib_dir', type=str, nargs=1, help='directory to store calibration settings in')
    parser.add_argument('-x', '--xcorners', type=int, nargs=1, default=8, help='horizontal dimension of checkerboard in square corners', dest='xcrns')
    parser.add_argument('-y', '--ycorners', type=int, nargs=1, default=6, help='vertical dimension of checkerboard in square corners', dest='ycrns')

    return parser

class ImSource():
    def __init__(self, crn_dimen=(8,6), name='camera calibration'):
        self.name = name
        self.win = cv2.namedWindow(self.name, cv2.WINDOW_OPENGL)

        self.crn_dimen = crn_dimen

        #lists to store object and image points for all images
        self.objpoints = []
        self.imgpoints = []

    def load_img(self, path):
        img = cv2.imread(os.path.join(path))
        return img

    def show_img(self, img):
        cv2.imshow(self.name, img)

def load_meta(path):
    with open(os.path.join(path), 'rb') as metaf:
        metadata = pickle.load(metaf)
    return metadata

if __name__ == "__main__":
    parser = argp_init()
    args = parser.parse_args()
    #get dir with images of checkerboard from argparse
    DATA_DIR = os.path.join(args.data_dir[0])

    CALIB_DIR = os.path.join(args.calib_dir[0])

    #create objects for each camera
    left = ImSource(crn_dimen=(args.xcrns, args.ycrns), name='left')
    right = ImSource(crn_dimen=(args.xcrns, args.ycrns), name='right')

    #termination criteria(when object point estimate is good enough)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    #prepare object points
    objp = numpy.zeros((numpy.product(left.crn_dimen), 3), numpy.float32)
    objp[:, :2] = numpy.indices(left.crn_dimen).T.reshape(-1, 2)

    #set num of image pairs to calibrate on to num of images in left camera directory, should be equal for right camera
    NUM_PAIRS = len(os.listdir(os.path.join(DATA_DIR, 'left')))

    inpkey = None

    #loop through each image of each pair
    for paircount in range(NUM_PAIRS):
        for side in left, right:

            #load image
            impath = os.path.join(DATA_DIR, side.name, str(paircount)+'.jpg')
            print(side.name, str(paircount))
            img = side.load_img(impath)

            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            h, w = grey.shape[:2]

            #find checkerboard squares' corners
            _, corners = cv2.findChessboardCorners(grey, side.crn_dimen, None)
            #if corners found, add object and image points
            if _ is True:
                print('valid image, processing')
                cv2.imwrite(impath, img)

                cv2.cornerSubPix(grey, corners, (5, 5), (-1, -1), criteria)
                side.imgpoints.append(corners.reshape(-1, 2))
                side.objpoints.append(objp)

                #Show corner predictions on images
                cv2.drawChessboardCorners(img, side.crn_dimen, corners, _)
                cv2.imshow(side.name, img)
                inpkey = cv2.waitKey(1000)
            else:
                print('image useless')
                inpkey = cv2.waitKey(1)

        #quit if q hit
        if inpkey == ord('q'):
            break

    cv2.destroyAllWindows()

    dec = input('save calib data? (y/n): ')
    print('generating calibration settings')
    #calibrate cameras
    for side in left, right:
        result = cv2.calibrateCamera(objectPoints=side.objpoints, imagePoints=side.imgpoints, imageSize=(w, h), cameraMatrix=None, distCoeffs=None)
        _, camMtx, distco, rvecs, tvecs = result

        dataset = (camMtx, distco, rvecs, tvecs)
        print('dataset made')

        if dec.lower() == 'y':
            #save calibration data in numpy data file
            numpy.save(os.path.join(CALIB_DIR, 'calib_settings_'+side.name), dataset)

            #save pickled points used for calibration to file
            with open(os.path.join(CALIB_DIR, 'points'+side.name), 'wb') as pointsf:
                pickle.dump((side.objpoints, side.imgpoints), pointsf)
        else:
            print('aborting')
