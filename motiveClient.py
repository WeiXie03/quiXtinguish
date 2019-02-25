import sys
import socket
import numpy as np
import cv2
import keyboard as kb
from data_collection.receivewrite2 import *
from time import sleep

HOST = input('Enter IP address of RPi: ')
PORT = 3027
TIMEOUT_SECONDS = 1e-3

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    sock.settimeout(TIMEOUT_SECONDS)
    #sock.connect((HOST, PORT))
    print('connected to RPi at', HOST, 'on port', PORT)
    left = Cam(5000, 'left', make_win=False)
    right = Cam(5200, 'right', make_win=False)
    window = cv2.namedWindow('window', cv2.WINDOW_OPENGL)
    #cv2.startWindowThread()
    print('?')
    #cmds = ['fw', 0, 90, 90] #initial settings
    curServoAngles = [90, 90]
    while True:
        try:
            curServoAngles = sock.recv(1024).decode()
        except socket.timeout as e:
            pass
        except socket.error as e:
            print(e)
            sys.exit(1)
        else:
            curServoAngles = curServoAngles.split(',')

        frames = []
        for stream in (left, right):
            _, frame = stream.cap.read()
            frames.append(frame)

        cv2.imshow('window', np.hstack(frames))

        key_hit = cv2.waitKey(20)
        '''
        print(key_hit)
        if not key_hit == -1:
            sleep(0.001)
        '''

        cmds = [None, None, None, None]
        if key_hit == ord('w'):
            cmds[0] = 'fw'
        elif key_hit == ord('s'):
            cmds[0] = 'bw'
        elif key_hit == ord('a'):
            cmds[0] = 'l'
        elif key_hit == ord('d'):
            cmds[0] = 'r'
        else:
            cmds[0] = 'pause'

        cmds[1] = 40 #setting speed to 40% of max for now

        targetAngles = curServoAngles.copy()
        if key_hit == ord('q'):
            targetAngles[0] -= 1
        elif key_hit == ord('e'):
            targetAngles[0] += 1
        elif key_hit == ord('r'):
            targetAngles[1] += 1
        elif key_hit == ord('f'):
            targetAngles[1] -= 1

        cmds[2] = targetAngles[0]
        cmds[3] = targetAngles[1]
        cmdsBytes = ','.join(str(cmds)).encode()

        print(cmds)
        #sock.sendto(cmdsBytes, (HOST, PORT))
