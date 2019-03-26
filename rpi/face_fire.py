import rpi.motiveServer as motion
import cv2
#from data_collection.writeframes import *
import sys
import os
import math

def point_click(event, x, y, flags, win):
    #shape of a mat object is height, width, channel
    req_disp = win.img.shape[1]/2 - x
    req_angle = math.degrees(math.atan(req_disp/win.focl))

class Window():
    def __init__(self, img_path, calib_mtx, name='view'):
        self.name = name
        self.win = cv2.namedWindow(name, cv2.WINDOW_OPENGL)
        self.img = self.load_img(img_path)

        self.focl = calib_mtx[?]
        self.win.setMouseCallback(self.name, point_click, self.img)

    def load_img(self, img_path):
        img = cv2.imread(img_path)
        cv2.imshow(self.name, img)

'''
def load_calib(path):
    with open(path, 'rb') as calibf:
'''

if __name__ == "__main__":
    try:
        print('enter file path of image, camera calibration file as command line arguments')
        IMG_PATH = os.path.join(sys.argv[1])
        CALIB_PATH = os.path.join(sys.argv[2])

        win = Window(IMG_PATH, load_calib(CALIB_PATH))

    finally:
        cv2.destroyAllWindows()
