import numpy
import cv2
import os
import pickle
import sys
import writeframes

class Cam():
    def __init__(self, port, name, make_win=True):
        self.name = name
        self.cap = cv2.VideoCapture('udpsrc port={} ! application/x-rtp,payload=96,media=video,encoding-name=H264 ! rtph264depay ! decodebin ! videoconvert ! appsink'.format(port), cv2.CAP_GSTREAMER)
        #video streaming from RPi to local stdin via netcat now
        #self.cap = cv2.VideoCapture("/dev/stdin")
        #self.cap = cv2.VideoCapture("udp://127.0.0.1:{}".format(port))
        print("Finished getting cap")
        if make_win:
            self.win = cv2.namedWindow(self.name, cv2.WINDOW_OPENGL)

if __name__ == "__main__":
    DATA_DIR = os.path.join(sys.argv[1])
    print('Setting up cams')
    stream = writeframes.Cam(6300, 'NoIR')
    print('Setup complete')

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
        _, frame = stream.cap.read()
        cv2.imshow(stream.label, frame)
        key_hit = cv2.waitKey(1)

        if key_hit == 32: #space bar
            metadata_entry = {}
            metadata_entry[stream.label] = {}
            img_path = os.path.join(DATA_DIR, stream.label,
                    "{}.jpg".format(im_count))
            metadata_entry[stream.label]["img_path"] = img_path
            cv2.imwrite(img_path, frame)
            print('wrote ', img_path, im_count)

            metadata[im_count] = metadata_entry
            im_count += 1

            '''
            with open(metadata_path+'d', 'wb') as metadataf:
                pickle.dump(metadata, metadataf)
            '''

        elif key_hit == ord('q'):
            break

    with open(metadata_path, 'wb') as metadataf:
        pickle.dump(metadata, metadataf)

    #When everything done, release the capture
    stream.cap.release()
    cv2.destroyAllWindows()
