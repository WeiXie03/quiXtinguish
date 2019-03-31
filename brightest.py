import numpy, cv2
import os, sys, pickle
from enum import Enum
import data_collection.writeframes as stream
import click2pan as direc
import socket
import math

class Window():
    def __init__(self, cam_mtx, angle_step=0.5, srch_rad=29):
        self.cam_mtx = cam_mtx

        self.radius = srch_rad
        self.angstep = angle_step

    def show_spot(self, winname, img, coords):
        #show brightest spot, bspot is pair of coords
        cv2.circle(img, coords, self.radius, (50, 50, 255), 2)
        cv2.imshow(winname, img)

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
        print(x-self.angstep)
        if x < img.shape[1]/2-5:
            print(1/8+abs(x)/(img.shape[1]/32))
            return max(-1*self.angstep*(1/8+abs(x)/(img.shape[1]/8)), -15)
        elif x > img.shape[1]/2+5:
            print(1/8+abs(x)/(img.shape[1]/64))
            return min(self.angstep*(1/8+abs(x)/(img.shape[1]/8)), 15)
            #return max(self.angstep)
        else:
            return 0

    def calc_depth(self, lcoords, rcoords, baseline):
        foclx = self.cam_mtx[0][0]
        x_l, x_r = lcoords[0], rcoords[0]
        depth = (baseline*foclx)/(x_r-x_l)
        return depth

def compare(prev, cur, subtractor):
    prevmask = subtractor.apply(prev)
    curmask = subtractor.apply(cur)
    return curmask - prevmask

def load_meta(metadata_path, im_count):
    if os.path.isfile(metadata_path):
        with open(metadata_path, 'rb') as metadataf:
            metadata = pickle.load(metadataf)
    else:
        metadata = {}

    if len(metadata.keys()) > 0:
        im_count = max(metadata.keys()) + 1

    return metadata, im_count

def metadd(meta_entry, stream_name, datadir, imgind, frame):
    meta_entry[stream_name] = {}

    #path will be something like "data/dataset/left/45.jpg"
    img_path = os.path.join(datadir, stream_name, "{}.jpg".format(str(imgind)))
    print(img_path)
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
    #HOST = input('IP of RPi: ')
    HOST = "192.168.43.16"
    PORT = 3030

    BASELINE = 35.9/10**2

    nir = stream.Cam(6300, 'NoIR')
    left = stream.Cam(5200, 'left')
    right = stream.Cam(5000, 'right')
    print('cameras set up')

    #load the metadata, holds img paths and other things in dictionaries
    metadata_path = os.path.join(DATA_DIR, 'metadata.dat')
    exp_count = 0
    metadata, exp_count = load_meta(metadata_path, exp_count)

    print('Starting')
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(('', PORT))
        sock.setblocking(0)

        #create window object
        win = Window(numpy.load(CALIB_PATH), srch_rad=BRIGHT_RADIUS)

        key_hit = None
        while(key_hit != ord('q')):
            _, nir_frame = nir.cap.read()
            _, lframe = left.cap.read()
            _, rframe = right.cap.read()
            #print('updated')

            key_hit = cv2.waitKey(1)
            '''
            if key_hit == 32: #space bar
                for ind in range(4):
                # Want these to happen consecutive
                    _, frame = nir.cap.read()
                    w_, wastefr = nir.cap.read()

                    metadata_entry = {}
                    metadd(metadata_entry, nir.label, DATA_DIR, im_count, frame)
                    metadata[im_count] = metadata_entry

                    im_count += 1

                    #backup
                    with open(metadata_path+'d', 'wb') as metadataf:
                        pickle.dump(metadata, metadataf)
            '''

            bspot = win.find_brightest(nir_frame)
            win.show_spot(nir.label, nir_frame, bspot)
            #find brightest point, show it on current frame

            try:
                cur_ang, (HOST, PORT) = sock.recvfrom(1024)
                cur_ang = float(cur_ang.decode())
                print(cur_ang)
            except BlockingIOError as e:
                #print(e)
                continue
            except ValueError:
                print(ValueError)
                continue
            else:
                #calculate and send angle to pan to to RPi

                print(cur_ang)
                try:
                    while True:
                        cur_ang, (HOST, PORT) = sock.recvfrom(1024)
                        cur_ang = float(cur_ang.decode())
                except BlockingIOError as e:
                    pass

                for i in range(15):
                    nir.cap.read()
                _, frame = nir.cap.read()

                print(cur_ang)
                #print('updated')

                bspot = win.find_brightest(frame)
                #check whether fire is in +/- 3 px of middle of view/frame
                if bspot[0]<frame.shape[1]/2+3 and bspot[0]>frame.shape[1]/2-3:
                    print('good enough')
                    break
                incre = win.cmd_pan(frame, bspot)
                sock.sendto(str(cur_ang-incre).encode(), (HOST, PORT))

        '''
        for cam in left, right:
            #make windows for left and right that will display difference between consecutive frames
            cam.diffwin = cv2.namedWindow(cam.label+' diff', cv2.WINDOW_OPENGL)

            _, frame = cam.cap.read()

            #find brightest point, show it on current frame
            bspot = win.find_brightest(frame)
            win.show_spot(cam.label, frame, bspot)
            cam.prev = frame
        '''

        key_hit = None
        DELAY_FRAMES = 5

        while(key_hit != ord('q')):
            _, lframe = left.cap.read()
            _, rframe = right.cap.read()
            _, nirframe = nir.cap.read()

            print(win.calc_depth(win.find_brightest(lframe), win.find_brightest(rframe), BASELINE), 'meters')

            key_hit = cv2.waitKey(1)
            if key_hit == 32:

                metadata_entry = {left.label:{'img_paths':[]}, right.label:{'img_paths':[]}, nir.label:{'img_paths':[]}}
                for frame_count in range(4):
                    _, lframe = left.cap.read()
                    _, rframe = right.cap.read()
                    _, nirframe = nir.cap.read()

                    for cam, frame in (left, lframe), (nir, nirframe), (right, rframe):
                        #path will be something like "data/dataset/45_2_left.jpg"
                        img_path = os.path.join(DATA_DIR, "{}_{}_{}.jpg".format(str(exp_count), str(frame_count), cam.label))
                        print(img_path)
                        #enter path in metadata as dictionary value for the stream(left, right or nir)
                        metadata_entry[cam.label]["img_paths"].append(img_path)

                        #actually save frame to file
                        cv2.imwrite(img_path, frame)
                        print('wrote ', img_path, frame_count)

                    for _ in range(DELAY_FRAMES):
                        _, _ = left.cap.read()
                        _, _ = right.cap.read()
                        _, _ = nir.cap.read()

                metadata[exp_count] = metadata_entry
                exp_count += 1

            for cam, frame in (left, lframe), (right, rframe), (nir, nirframe):

                #diff = compare(cam.prev, frame, kompar)
                #cv2.imshow(cam.label+' diff', diff)

                '''
                #show the difference in consecutive frames for each camera
                diff = numpy.abs(frame.astype(numpy.int8) - cam.prev.astype(numpy.int8)).astype(numpy.uint8)
                cv2.imshow(cam.label+' diff', diff)

                cam.prev = frame
                '''

                #find brightest point, show it on current frame
                bspot = win.find_brightest(frame)
                win.show_spot(cam.label, frame, bspot)

    with open(metadata_path, 'wb') as metadataf:
        pickle.dump(metadata, metadataf)

    #When everything done, release the capture
    for cam in nir, left, right:
        cam.cap.release()
    cv2.destroyAllWindows()
