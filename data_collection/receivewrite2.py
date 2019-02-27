import numpy
import cv2
import os
import pickle

class Cam(object):
    def __init__(self, port, side, make_win=True):
        self.side = side
        self.cap = cv2.VideoCapture('udpsrc port=' + str(port) + ' ! application/x-rtp,media=video,payload=26,encoding-name=JPEG ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink', cv2.CAP_GSTREAMER)
        if make_win:
            self.win = cv2.namedWindow(self.side, cv2.WINDOW_OPENGL)

if __name__ == "__main__":
    DATA_DIR = 'data/perm2/'
    streaml = Cam(5200, 'left')
    streamr = Cam(5000, 'right')

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

    while(True):
        key_hit = None
        for stream in (streaml, streamr):
            _, frame = stream.cap.read()
            cv2.imshow(stream.side, frame)
        key_hit = cv2.waitKey(1)

        if key_hit == 32: #space bar
            # Want these to happen consecutive
            _, framel = stream.cap.read()
            _, framer = stream.cap.read()

            metadata_entry = {}
            for stream, frame  in [(streaml, framel), (streamr, framer)]:
                metadata_entry[stream.side] = {}
                img_path = os.path.join(DATA_DIR, stream.side,
                        "{}.jpg".format(str(im_count)))
                metadata_entry[stream.side]["img_path"] = img_path
                cv2.imwrite(img_path, frame)
                print('wrote ', im_count)
            im_count += 1

            metadata[im_count-1] = metadata_entry

        elif key_hit == ord('q'):
            break

    with open(metadata_path, 'wb') as metadataf:
        pickle.dump(metadata, metadataf)

    #When everything done, release the capture
    for stream in (streaml, streamr):
        stream.cap.release()
    cv2.destroyAllWindows()
