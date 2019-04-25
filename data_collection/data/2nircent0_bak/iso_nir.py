import numpy as np
import cv2
import sys, os

def process_img(img):
    '''
    Extracts red channel(only NIR light because of blue filter) and converts to greyscale, NIR intensity map
    '''
    red = img[:,:,2]
    #intensity = cv2.cvtColor(red, cv2.COLOR_BGR2GRAY)

    return red

if __name__ == "__main__":
    print('enter data directory(one with images) as command line arg')
    DATA_DIR = sys.argv[1]

    #make window
    win = cv2.namedWindow('Near Infrared Intensity', cv2.WINDOW_AUTOSIZE)

    imind = None
    while imind != 'q':
        imind = input('enter index of image pair to process or \'q\' to quit: ')
        imind = int(imind)

        #get image pair to use
        limg, rimg = cv2.imread(os.path.join(DATA_DIR, 'left', str(imind)+'.jpg')), cv2.imread(os.path.join(DATA_DIR, 'right', str(imind)+'.jpg'))

        #process
        limg, rimg = process_img(limg), process_img(rimg)

        print('processed image pair', imind, ', displaying\nhit any key to stop displaying')
        #display
        tog = np.hstack((limg, rimg))
        cv2.imshow('Near Infrared Intensity', tog)
        cv2.waitKey(0)
