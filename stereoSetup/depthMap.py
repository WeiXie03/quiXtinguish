import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import sys

imgL = cv.imread(sys.argv[1],0)
#cv.imshow('left', imgL)
imgR = cv.imread(sys.argv[2],0)
#cv.imshow('right', imgR)
cv.imshow('lr', np.hstack((imgL, imgR)))

if cv.waitKey(10000):
    stereo = cv.StereoBM_create(blockSize=29) #create OpenCV stereo object
    disparity = stereo.compute(imgL,imgR) #generate disparity map(image) using stereo object
    plt.imshow(disparity,'gray')
    plt.show()

cv.destroyAllWindows()
