import numpy
import cv2
import time

class CamWin(cv2.namedWindow):

    streams = []
    imCount = 0
    baseDist =

    def __init__(self, camStream, side): #camStream is the cv2.VideoCapture object that represents a video stream
        CamWin.streams.append(self)
        self.side = side #side is simply 'left' or 'right'
        self.writeDir = raw_input('Enter the path of the directory where you would like to save images(' + self.side + ' cam)')
        super(CamWin, self).__init__(self.side, cv2.WINDOW_OPENGL)

    def dispFrame(self, frame):
        # Capture frame-by-frame

        '''
        # shrink the images to half size
        frame0 = cv2.resize(frame0,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
        frame1 = cv2.resize(frame1,None,fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
        '''

        #display the camera streams
        cv2.imshow(self.side, frame)

    def clicked(self, event, x, y, flags, frame):
        if event == cv2.EVENT_LBUTTONDOWN:
            cv2.circle(img,(x,y),100,(255,0,0),-1)
            print('mouse coordinates(x, y): 'x, ',', y, '\tpoint depth = ', )

            cv2.imwrite(self.writeDir + self.side + str(CamWin.imCount), frame)
            imCount += 1
            print('wrote ' + self.side + ' frame to ', self.writeDir)

if __name__ == "__main__":
    #receive video packaged in RTP packets from gstreamer on Raspi over UDP
    cap0 = cv2.VideoCapture('udpsrc port=5200 ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink',cv2.CAP_GSTREAMER)
    cap1 = cv2.VideoCapture('udpsrc port=5000 ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink',cv2.CAP_GSTREAMER)

    #create the window objects(class defined above)
    win0 = CamWin(cap0, 'right')
    win1 = CamWin(cap1, 'left')

    while(True):
        #loop through all camera streams
        for stream in CamWin.streams:
            isRec, frame = stream.cap.read()
            stream.dispFrame(frame)
            stream.setMouseCallback(stream.side, stream.clicked, frame)

        if cv2.waitKey == ord('q'):
            break
            print('quit capturing')

#When everything done, release the capture
cap0.release()
cap1.release()
cv2.destroyAllWindows()
