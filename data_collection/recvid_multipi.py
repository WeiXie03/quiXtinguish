import numpy
import cv2
import os, sys
import pickle
from enum import Enum

class Codec(Enum):
    MJPEG=0
    MJPG=0
    JPEG=0
    JPG=0
    H264=1
    X264=1

class Cam():
    def __init__(self, port, label, codec=Codec.MJPEG, make_win=True):
        self.label = label

        print(codec)
        if codec == Codec.H264:
            #get gStreamer stream from RPi on UDP, video is mjpeg, using rtp
            self.cap = cv2.VideoCapture('udpsrc port={} ! application/x-rtp,payload=96,media=video,encoding-name=H264 ! rtph264depay ! decodebin ! videoconvert ! appsink'.format(port), cv2.CAP_GSTREAMER)
        elif codec == Codec.MJPEG:
            #same as above, but using MJPEG
            self.cap = cv2.VideoCapture("udpsrc port={} ! application/x-rtp, encoding-name=JPEG, payload=26 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink".format(port), cv2.CAP_GSTREAMER)
        print(self.cap)

        if make_win:
            self.win = cv2.namedWindow(self.label, cv2.WINDOW_OPENGL)

    def __repr__(self):
        return 'stream of {} camera, receiving stream through {}'.format(self.label, self.cap)

if __name__ == "__main__":
    print('data directory is command line argument after this python program\'s name')
    DATA_DIR = sys.argv[1]

    streaml = Cam(5400, 'left')
    streamr = Cam(5800, 'right')
    print('cameras set up')

    #storing stuff like image file location and coordinates of the fire in a bunch of dictionaries in an encoded(bytes) metadata file
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    metadata = None
    if os.path.isfile(metadata_path):
        with open(metadata_path, 'rb') as metadataf:
            metadata = pickle.load(metadataf)
    else:
        metadata = {}

    im_count = 0
    if len(metadata.keys()) > 0:
        im_count = max(metadata.keys()) + 1

    print('Starting')
    while(True):
        key_hit = None

        #want these to happen consecutively
        _, framel = streaml.cap.read()
        _, framer = streamr.cap.read()

        tog = numpy.hstack((framel, framer))
        cv2.imshow(streaml.label + ',' + streamr.label, tog)

        key_hit = cv2.waitKey(1)
        if key_hit == 32: #space bar
            # Want these to happen consecutive
            _, framel = streaml.cap.read()
            _, framer = streamr.cap.read()

            metadata_entry = {}
            for stream, frame  in ((streaml, framel), (streamr, framer)):
                metadata_entry[stream.label] = {}

                #path will be something like "data/dataset/left/45.jpg"
                img_path = os.path.join(DATA_DIR, stream.label, "{}.jpg".format(str(im_count)))
                #enter path in metadata as value for label(left, right or nir)
                metadata_entry[stream.label]["img_path"] = img_path

                #actually save frame to file
                cv2.imwrite(img_path, frame)
                print('wrote ', img_path, im_count)

            metadata[im_count] = metadata_entry

            '''
            with open(metadata_path+'d', 'wb') as metadataf:
                pickle.dump(metadata, metadataf)
            '''

            im_count += 1

        elif key_hit == ord('q'):
            break

    with open(metadata_path, 'wb') as metadataf:
        pickle.dump(metadata, metadataf)

    #When everything done, release the capture
    for stream in streaml, streamr:
        stream.cap.release()
    cv2.destroyAllWindows()
