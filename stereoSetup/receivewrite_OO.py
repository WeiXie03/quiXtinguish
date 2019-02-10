import numpy
import cv2
import pdb

#pdb.set_trace()

class Cam(object):

    streams = []
    imWriteDir = 'camsSetPerm_channel/'
    imCount = 0
    #baseDist =

    def __init__(self, port, side): #camStream is the cv2.VideoCapture object that represents a video stream
        self.side = side #side is simply 'left' or 'right'
        #self.imWriteDir = './data/' + input('Enter the path of the directory within the data directory where you would like to save images(' + self.side + ' cam). You should create two directories, one for left, one for right.\n\t') + '/'

        #receive video packaged in RTP packets from gstreamer on Raspi over UDP
        self.cap = cv2.VideoCapture('udpsrc port=' + str(port) + ' ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        print(self.cap)

        #create the window to display live stream with OpenGL support ahead of time
        self.win = cv2.namedWindow(self.side, cv2.WINDOW_OPENGL)

        #cv2.setMouseCallback(self.side, clicked)

        Cam.streams.append(self)

'''
        self.txtWriteDir = input('Enter the path of the directory where you would like to save text supplementing images(' + self.side + ' cam)')
        self.datxt = open(txtWriteDir + '/images_supplement_' + self.side + '.txt')'''

#decided to move mouse business to another program
'''
def clicked(winName, event, x, y, flags):
    global frame
    print(frame)
    if event == cv2.EVENT_LBUTTONDOWN:
        #draw a circle around the mouse, print its coordinates in the image
        cv2.circle(frame,(x,y),100,(255,0,0),-1)
        print('mouse coordinates(x, y): ', x, ', ', y, '\tpoint depth = ')

        #calculate depth of corresponding point on both sides according to the equation from here:

        cv2.imwrite('./data/' + Cam.imWriteDir + winName + '/' + str(Cam.imCount), frame)
        Cam.imCount += 1
        print('wrote ' + winName + ' to ', Cam.imWriteDir)
'''

if __name__ == "__main__":
    #create the window objects(class defined above)
    stream0 = Cam(5200, 'right')
    stream1 = Cam(5000, 'left')
    print(Cam.streams)

    while(True):
        isRec0, frame0 = stream0.cap.read()
        isRec1, frame1 = stream1.cap.read()
        #print(isRec)

        cv2.imshow(stream0.side, frame0) #display the camera streams
        cv2.imshow(stream1.side, frame1)
        keyHit = cv2.waitKey(1)

        if keyHit == 32:
            cv2.imwrite('./data/' + Cam.imWriteDir + stream0.side + '/' + str(Cam.imCount) + '.jpg', frame0) #filename comes out to be something like ./data/test/left/3.jpg
            cv2.imwrite('./data/' + Cam.imWriteDir + stream1.side + '/' + str(Cam.imCount) + '.jpg', frame1)
            Cam.imCount += 1
            print('wrote both')

        elif keyHit == ord('q'):
            break
            print('quit capturing')

#When everything done, release the capture
for stream in Cam.streams:
    stream.cap.release()
cv2.destroyAllWindows()
