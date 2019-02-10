import cv2
import numpy
import json
import pdb

#pdb.set_trace()

class App(object):

    datDir = 'camsSetPerm_channel'
    #datDir = input('Enter the path of the directory where the left and right images, and text data are saved.\n ')
    imNum = input('Enter the image number indicated in the names of the left right image pair you would like to use.\n ')
    imgs = []
    jdat = open('./data/' + datDir + '/data.json')

    def __init__(self, side):
        self.side = side
        self.img = cv2.imread('./data/' + App.datDir + '/' + self.side + '/' + App.imNum + '.jpg')
        self.win = cv2.namedWindow(self.side, cv2.WINDOW_OPENGL)

        cv2.setMouseCallback(self.side, clicked, self)
        self.finClick = False

        #self.supDat = {left:{}, right:{}}

        App.imgs.append(self)

def clicked(event, x, y, flags, pole):
    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(pole.img, (x,y), 20, (234, 240, 255), -1)
        print('x: ', x, ', y: ', y)

        #saveDat(x, y)

        pole.finClick = True

#def saveDat(x, y):
    #saves coordinates of mouse, disparity and calculated depth to json file

if __name__ == "__main__":

    left = App('left')
    right = App('right')

    print(App.imgs)
    for pole in App.imgs:
        cv2.imshow(pole.side, pole.img)
        while(pole.finClick == False):
            keyHit = cv2.waitKey(1)
            if keyHit == ord('q'):
                break

cv2.destroyAllWindows()
App.jdat.close()
