import rpi.motiveServer as motion
import cv2
#from data_collection.writeframes import *
import sys
import os

def point_click(img):


class Window():
    def __init__(self, img_path, name='view'):
        self.name = name
        self.win = cv2.namedWindow(name, cv2.WINDOW_OPENGL)
        self.img = self.load_img(img_path)

        self.win.setMouseCallback(self.name, point_click, self.img)

    def load_img(self, img_path):
        img = cv2.imread(img_path)
        cv2.imshow(self.name, img)

if __name__ == "__main__":
    print('enter file path of image as command line argument')
    IMG_PATH = os.path.join(sys.argv[1])

    win = Window(IMG_PATH)

