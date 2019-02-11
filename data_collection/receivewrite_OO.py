import numpy
import cv2
import pdb
import json

#pdb.set_trace()

class Cam(object):

    streams = []
    datDir = 'camsSetPerm_channel/'
    imCount = 1
    supDat = {}

    def __init__(self, port, side): #camStream is the cv2.VideoCapture object that represents a video stream
        self.side = side #side is simply 'right' or 'left'
        #self.datDir = './data/' + input('Enter the path of the directory within the data directory where you would like to save images(' + self.side + ' cam). You should create two directories, one for right, one for left.\n\t') + '/'

        #receive video packaged in RTP packets from gstreamer on Raspi over UDP
        self.cap = cv2.VideoCapture('udpsrc port=' + str(port) + ' ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        #print(self.cap)

        #create the window to display live stream with OpenGL support ahead of time
        self.win = cv2.namedWindow(self.side, cv2.WINDOW_OPENGL)

        #cv2.setMouseCallback(self.side, clicked) #decided to move mouse business to another program

        Cam.streams.append(self)

def writeImg(stream, frame):
    imLoc = './data/' + Cam.datDir + stream.side + '/' + str(Cam.imCount) + '.jpg' #filename comes out to be something like ./data/test/right/3.jpg
    cv2.imwrite(imLoc, frame)
    print('wrote', stream.side)
    Cam.supDat[Cam.imCount][stream.side]['loc'] = imLoc

if __name__ == "__main__":
    #create the window objects(class defined above)
    stream0 = Cam(5200, 'left')
    stream1 = Cam(5000, 'right')
    #print(Cam.streams)

    jDatf = open('./data/' + Cam.datDir + 'data.json', 'r+') #open JSON file for writing
    #print(jDatf)
    jDat = json.load(jDatf)
    print(jDat, '\ti')
    if len(jDat) > 0:
        Cam.imCount = int(sorted(jDat)[-1]) + 1 #set imCount to 1 greater than the last entry

    #spacHit = False

    while(True):
        Cam.supDat[Cam.imCount] = {} #add a new entry in the JSON file for the image pair to be created
        for stream in Cam.streams:
            isRec, frame = stream.cap.read()
            cv2.imshow(stream.side, frame) #display the camera streams
            keyHit = cv2.waitKey(1)
            Cam.supDat[Cam.imCount][stream.side] = {}

        if keyHit == 32:
            for stream in Cam.streams:
                writeImg(stream, frame)
                #json dict managed in writeImg()
            Cam.imCount += 1

            print(Cam.supDat)
            print(jDat)
            jDat.append(Cam.supDat)
            json.dump(Cam.supDat, jDatf, indent=4)

        elif keyHit == ord('q'):
            break
            print('quit capturing')

    jDatf.close()
#When everything done, release the capture
for stream in Cam.streams:
    stream.cap.release()
cv2.destroyAllWindows()
