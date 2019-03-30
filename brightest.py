import numpy, cv2
import os, sys, pickle
from enum import Enum
import data_collection.writeframes as stream
import click2pan as direc
import socket
import math

class Window():
    def __init__(self, stream, cam_mtx, angle_step=0.5, srch_rad=29):
        #will use stream/camera's window
        self.stream = stream
        self.cam_mtx = cam_mtx

        self.radius = srch_rad
        self.angstep = angle_step

    def show_spot(self, img, coords):
        #show brightest spot, bspot is pair of coords
        cv2.circle(img, coords, self.radius, (50, 50, 255), 2)
        cv2.imshow(self.stream.label, img)

    def find_brightest(self, img):
        #convert to greyscale
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        grey = cv2.GaussianBlur(grey, (self.radius, self.radius), 0)
        #use Gaussian blur to average out everything and supress random bright spots(eg. lights)
        (min_val, max_val, min_loc, max_loc) = cv2.minMaxLoc(grey)
        #circle the spot

        return max_loc

    '''
    def calc_pan(self, img, coords):
        x, foclx = coords[0], self.cam_mtx[0][0]
        req_disp = img.shape[1]/2 - (x-img.shape[1]/2)
        req_angle = math.degrees(math.atan(req_disp/foclx)) + 55

        return req_angle
    '''

    def cmd_pan(self, img, coords):
        x = coords[0]
        if x < img.shape[1]/2:
            return -1*self.angstep
        elif x > img.shape[1]/2:
            return self.angstep
        else:
            return 0

def load_meta(metadata_path, im_count):
    if os.path.isfile(metadata_path):
        with open(metadata_path, 'rb') as metadataf:
            metadata = pickle.load(metadataf)
    else:
        metadata = {}

    if len(metadata.keys()) > 0:
        im_count = max(metadata.keys()) + 1

    return metadata, im_count

def metadd(meta_entry, stream_name, datadir, imgind):
    meta_entry[stream_name] = {}

    #path will be something like "data/dataset/left/45.jpg"
    img_path = os.path.join(datadir, stream_name, "{}.jpg".format(str(imgind)))
    #enter path in metadata as dictionary value for the stream(left, right or nir)
    meta_entry[stream_name]["img_path"] = img_path

    #actually save frame to file
    cv2.imwrite(img_path, frame)
    print('wrote ', img_path, imgind)

if __name__ == "__main__":
    print('data directory, calibrated mtx path are command line args')
    DATA_DIR = sys.argv[1]
    #radius for the brightest spot search
    BRIGHT_RADIUS = 29 #pixels
    CALIB_PATH = sys.argv[2]
    HOST = input('IP of RPi: ')
    PORT = 3030

    nir = stream.Cam(6300, 'NoIR', stream.Codec.H264)
    print('cameras set up')

    #load the metadata, holds img paths and other things in dictionaries
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    im_count = 0
    metadata, im_count = load_meta(metadata_path, im_count)

    socket.setdefaulttimeout(0.005)
    print('Starting')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', PORT))
        #little test
        #sock.sendto(b'connected', (HOST, PORT))

        #create window object
        win = Window(nir, numpy.load(CALIB_PATH), srch_rad=BRIGHT_RADIUS)

        key_hit = None
        while(key_hit != ord('q')):
            _, frame = nir.cap.read()
            print('updated')

            bspot = win.find_brightest(frame)
            win.show_spot(frame, bspot)
            #find brightest point, show it on current frame

            key_hit = cv2.waitKey(1)
            if key_hit == 32: #space bar
                # Want these to happen consecutive
                _, frame = nir.cap.read()

                metadata_entry = {}
                metadd(metadata_entry, nir.label, DATA_DIR, im_count)
                metadata[im_count] = metadata_entry

                im_count += 1

                ''' backup
                with open(metadata_path+'d', 'wb') as metadataf:
                    pickle.dump(metadata, metadataf)
                '''

            try:
                cur_ang, (HOST, PORT) = sock.recvfrom(1024)
                cur_ang = float(cur_ang.decode())
                print(cur_ang)
            except socket.timeout as e:
                print(e)
                continue
            except ValueError:
                print(ValueError)
                continue
            else:
                #calculate and send angle to pan to to RPi
                incre = win.cmd_pan(frame, bspot)
                sock.sendto(str(incre).encode(), (HOST, PORT))

    with open(metadata_path, 'wb') as metadataf:
        pickle.dump(metadata, metadataf)

    #When everything done, release the capture
    nir.cap.release()
    cv2.destroyAllWindows()
