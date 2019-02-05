import numpy as np
import cv2 as cv
import glob
import pdb
#pdb.set_trace()

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

#specify the number of corners of the chessboard used, refer to OpenCV 3D calibration docs
yCrn = 9
xCrn = 6

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((xCrn*yCrn,3), np.float32)
objp[:,:2] = np.mgrid[0:yCrn,0:xCrn].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('./rawImgs/*.jpg')
#images = glob.glob('/home/wei/opencv-3.4.5/samples/data/left*')

#win = cv.namedWindow('img')

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    #cv.imshow(fname, gray)
    #cv.waitKey(60)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (yCrn,xCrn), None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)

        '''
        # Draw and display the corners
        cv.drawChessboardCorners(img,(yCrn,xCrn), corners2, ret)
        cv.imshow('img', img)
        cv.waitKey(5000)
        '''

#cv.destroyAllWindows()

#pdb.set_trace()

#use OpenCV's .calibrateCamera() to get translation vectors, distortion coefficients, etc. based on objpoints and imgpoints
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#img = cv.imread(images[0])
print(images)
for fname in images:
    img = cv.imread(fname)

    h, w = img.shape[:2]
    #refine camera matrix according to alpha value and get region of interest
    newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    #undistort Mat image object(a copy of the already-saved file) based on distortion of camera found earlier
    dst = cv.undistort(img, mtx, dist, None, newcameramtx)

    # crop the image and write(replace) it
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    #cv.imshow('img', dst)
    print(fname)
    if 'eft' in fname:
        cv.imwrite('./prcsdImgs/left' + fname[-9:-4] + '.png', dst)
    elif 'ght' in fname:
        cv.imwrite('./prcsdImgs/right' + fname[-9:-4] + '.png', dst)
    np.savez('calibSettings', newcameramtx, dist, rvecs, tvecs)
