import numpy
import cv2
import time

cap0 = cv2.VideoCapture('udpsrc port=5200 ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink',cv2.CAP_GSTREAMER)
#receive video packaged in RTP packets from Raspi over UDP
cap1 = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink',cv2.CAP_GSTREAMER)

#pre-define OpenGL windows for displaying streams
win0 = cv2.namedWindow('right', cv2.WINDOW_OPENGL)
win1 = cv2.namedWindow('left', cv2.WINDOW_OPENGL)

imCount = 0

while(cap0.isOpened(),cap1.isOpened()):
    # Capture frame-by-frame
    ret0, frame0 = cap0.read()
    print(ret0)
    ret1, frame1 = cap1.read()
    print(ret1)

    '''
    # shrink the images to half size
    frame0 = cv2.resize(frame0,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
    frame1 = cv2.resize(frame1,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
    '''

    #display the camera streams
    cv2.imshow('right',frame0)
    cv2.imshow('left',frame1)

    keyHit = cv2.waitKey(1)

    if keyHit & 0xFF == 32: #pass hexadecimal and ASCII code of the key pressed into an AND gate to only take the first 8 bits
        #if space bar pressed, save frame as image file
        cv2.imwrite('./roughDistTesting/right' + str(imCount) + '.jpg', frame0)
        cv2.imwrite('./roughDistTesting/left' + str(imCount) + '.jpg', frame1)
        print('written ', str(imCount + 1), ' images for each camera')

        imCount += 1

    elif keyHit & 0xFF == ord('q'): #if user hits q, stop capturing
        break

# When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()
