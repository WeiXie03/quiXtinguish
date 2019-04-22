import cv2, numpy
import os, sys, pickle
import argparse

def argp_init():
    parser = argparse.ArgumentParser(description="Calibrate two cameras for stereo vision using checkerboard pattern.")
    parser.add_argument('data_dir', type=str, nargs=1, help='directory containing stereo images of pattern')
    parser.add_argument('calib_dir', type=str, nargs=1, help='directory to store calibration settings in')
    parser.add_argument('-x', '--xcorners', type=int, nargs=1, default=8, help='horizontal dimension of checkerboard in square corners', dest='xcrns')
    parser.add_argument('-y', '--ycorners', type=int, nargs=1, default=6, help='vertical dimension of checkerboard in square corners', dest='ycrns')
    parser.add_argument('-rec', '--rectify', action='store_true', help='test rectification on last image pair used for calibration', dest='rectest')

    return parser

class ImSource():
    def __init__(self, crn_dimen=(8,6), name='camera calibration'):
        self.name = name
        self.win = cv2.namedWindow(self.name, cv2.WINDOW_AUTOSIZE)

        self.crn_dimen = crn_dimen

        #lists to store object and image points for all images
        self.objpoints = []
        self.imgpoints = []
        self.dataset = ()

    def load_img(self, path):
        img = cv2.imread(os.path.join(path))
        return img

    def show_img(self, img):
        cv2.imshow(self.name, img)

def rectify(camMtx, distcos, rot, proj, img):
    '''
    returns an undistortion of image img given the camera's intrinsics
    '''
    h, w = img.shape[:2]
    #print('in rectify, before actual rectification', img.shape)
    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix=camMtx, distCoeffs=distcos, R=rot, newCameraMatrix=proj, size=(w,h), m1type=5)

    undistim = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
    #print('in rectify after rectification', undistim.shape)

    return undistim

def sterectify(lmtx, ldist, rmtx, rdist, rot, trans, limg, rimg):
    '''
    Returns both corrected stereo images as ndarrays,
    Each data arg is a calibration dataset(attribute of ImSources)
    '''
    #print('rot mtx', rot, ', trans vect', trans)

    h, w = limg.shape[:2]
    #print('in sterectify, before', rimg.shape)
    #calculating rectification settings
    lrot, rrot, lproj, rproj, Q, lvalidROI, rvalidROI = cv2.stereoRectify(cameraMatrix1=lmtx, distCoeffs1=ldist, cameraMatrix2=rmtx, distCoeffs2=rdist, imageSize=(w,h), R=rot, T=trans, alpha=0, newImageSize=(0,0))

    #undistort images using same camera parameters from stereoRectify()
    finlimg = rectify(lmtx, ldist, lrot, lproj, limg)
    finrimg = rectify(rmtx, rdist, rrot, rproj, rimg)
    #print('in sterectify, after', finrimg.shape)

    return finlimg, finrimg

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
    #NUM_PAIRS = len(os.listdir(os.path.join(DATA_DIR, 'left')))
    NUM_PAIRS = 14

    inpkey = None

    #loop through each image of each pair
    for paircount in range(NUM_PAIRS):
        for side in left, right:

            #load image
            impath = os.path.join(DATA_DIR, side.name, str(paircount)+'.jpg')
            print(side.name, str(paircount))
            img = side.load_img(impath)

            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            print('grey', grey.shape)
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
                inpkey = cv2.waitKey(70)
            else:
                print('image useless')
                inpkey = cv2.waitKey(1)

        #quit if q hit
        if inpkey == ord('q'):
            break

    print('generating calibration settings')
    #calibrate cameras
    for side in left, right:
        _, camMtx, distco, rvecs, tvecs = cv2.calibrateCamera(objectPoints=side.objpoints, imagePoints=side.imgpoints, imageSize=(w,h), cameraMatrix=None, distCoeffs=None)

        side.dataset = (camMtx, distco, rvecs, tvecs)
        print(side.name, 'dataset made')

    #stereo calibration
    result = cv2.stereoCalibrate(objectPoints=left.objpoints, imagePoints1=left.imgpoints, imagePoints2=right.imgpoints, cameraMatrix1=left.dataset[0], distCoeffs1=left.dataset[1], cameraMatrix2=right.dataset[0], distCoeffs2=right.dataset[1], imageSize=(w,h), flags=cv2.CALIB_FIX_INTRINSIC)
    ster_dataset = tuple([result[i] for i in range(5,9)])
    #ster_dataset is (rotation matrix between two cameras, translation vector between cameras, essential matrix and fundamental matrix),
    #see https://docs.opencv.org/3.4.5/d9/d0c/group__calib3d.html#ga91018d80e2a93ade37539f01e6f07de5
    #print(dataset[:2])

    #if rectification test selected, display rectified image
    if args.rectest:
        print('rectifying')

        #get images
        pairnum = 0 #there's gotta be at least one image in the dir
        limpath = os.path.join(DATA_DIR, left.name, str(pairnum)+'.jpg')
        rimpath = os.path.join(DATA_DIR, right.name, str(pairnum)+'.jpg')
        limg, rimg = cv2.imread(limpath), cv2.imread(rimpath)

        print('before: left', limg.shape, ', right', rimg.shape)

        #rectify images
        limg, rimg = sterectify(left.dataset[0], left.dataset[1], right.dataset[0], right.dataset[1], ster_dataset[0], ster_dataset[1], limg, rimg)
        print('after: left', limg.shape, ', right', rimg.shape)

        print('showing rectified')
        cv2.imshow(left.name, limg)
        cv2.imshow(right.name, rimg)
        cv2.waitKey()

        #save undistorted test images
        dec = input('save undistorted images? (y/n): ')
        if dec.lower() == 'y':
            cv2.imwrite(os.path.join(DATA_DIR, left.name, str(pairnum)+'_undist.jpg'), limg)
            cv2.imwrite(os.path.join(DATA_DIR, right.name, str(pairnum)+'_undist.jpg'), rimg)
            print('saved images')
        else:
            print('skipping')
    cv2.destroyAllWindows()

    dec = input('save calib data? (y/n): ')
    if dec.lower() == 'y':
        #save calibration data in data file
        for side in left, right:
            numpy.save(os.path.join(CALIB_DIR, 'calib_settings_'+side.name), side.dataset)
        with open(os.path.join(CALIB_DIR, 'calib_settings_stereo.dat'), 'wb') as sterf:
            pickle.dump(ster_dataset, sterf)
    else:
        print('aborting')
