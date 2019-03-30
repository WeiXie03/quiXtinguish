import cv2
import os, sys
import brightest as fire

class Window():
    def __init__(self, name='fire detection'):
        self.name = name
        self.win = cv2.namedWindow(self.name)

    def show_fire(self, img, radius=5):
        bspot = fire.find_brightest(img, radius)
        print(bspot)
        #show brightest spot, bspot is pair of coords
        cv2.circle(img, bspot, radius, (100, 80, 80), 2)

        #update window with image whose fire is circled
        cv2.imshow(self.name, img)

if __name__ == "__main__":
    win = Window()

    print('enter path of image as command line arg')
    im_path = sys.argv[1]
    img = cv2.imread(im_path)

    radius = int(input('radius of detection circle in pixels: '))

    key_hit = None
    win.show_fire(img, radius)
    while key_hit != ord('q'):
        key_hit = cv2.waitKey(1)

    cv2.destroyAllWindows()
