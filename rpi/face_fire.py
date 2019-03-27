import rpi.motiveServer as motion
import cv2
#from data_collection.writeframes import *
import sys
import os
import math
import numpy as np
import socket

def load_calib(calib_path):
    #calibrated settings saved as a matrix in a NumPy file
    return np.load(calib_path)

if __name__ == "__main__":
    print('enter file path of image, camera calibration file as command line arguments')
    IMG_PATH = os.path.join(sys.argv[1])
    CALIB_PATH = os.path.join(sys.argv[2])

    HOST = "127.0.0.1"
    PORT = 6300

    robot = motion.Robot(name='FireBot')
    calib_mtx = load_calib(CALIB_PATH)
    #x focal length is first element in calibration matrix
    foclx = calib_mtx[0]

    try:
        #robot.rotate(90, 90)

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((HOST, PORT))
            sock.listen()
            conn, addr = sock.accept()
            with conn:
                while True:
                    try:
                        req_angle, addr = sock.recvfrom(1024)
                        req_angle = float(req_angle.decode())
                        print(req_angle)
                    except socket.timeout as e:
                        print(e)
                    except socket.error as e:
                        print(e)
                        sys.exit()
                    else:
                        #req_angle is a ref angle, need to add 90 deg
                        #win.bot.pan.turn(90 + req_angle)

    finally:
        robot.pi.write(robot.pan.pin, 0)
        '''
        robot.left.close()
        robot.right.close()
        robot.pi.write(robot.tilt.pin, 0)
        '''
        robot.pi.stop()
        print(robot.name, 'dead')
